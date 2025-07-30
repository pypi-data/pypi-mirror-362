from functools import partial, reduce
from itertools import filterfalse
from pathlib import Path

import networkx as nx
import rdflib
from networkx import DiGraph
from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS

from cemento.rdf.filters import term_in_search_results, term_not_in_default_namespace
from cemento.rdf.io import (
    get_diagram_terms_iter,
    get_diagram_terms_iter_with_pred,
    get_search_terms_from_defaults,
    get_search_terms_from_graph,
    get_ttl_file_iter,
    iter_diagram_terms,
    iterate_ttl_graphs,
    read_prefixes_from_graph,
    read_prefixes_from_json,
)
from cemento.rdf.preprocessing import (
    generate_residual_prefixes,
    get_abbrev_term,
    get_term_aliases,
    merge_dictionaries,
)
from cemento.rdf.transforms import (
    add_domains_ranges,
    add_exact_matches,
    add_labels,
    bind_prefixes,
    construct_literal,
    construct_term_uri,
    get_class_terms,
    get_doms_ranges,
    get_literal_data_type,
    get_term_search_keys,
    get_term_value,
    substitute_term,
    get_literal_lang_annotation
)


def convert_graph_to_ttl(
    graph: DiGraph,
    output_path: str | Path,
    onto_ref_folder: str | Path = None,
    prefixes_path: str | Path = None,
) -> None:
    default_namespaces = [RDF, RDFS, OWL, DCTERMS, SKOS]
    default_namespace_prefixes = ["rdf", "rdfs", "owl", "dcterms", "skos"]

    prefixes = dict()
    if prefixes_path:
        prefixes = read_prefixes_from_json(prefixes_path)

    default_namespace_prefixes = {
        prefix: ns for prefix, ns in zip(default_namespace_prefixes, default_namespaces)
    }
    prefixes.update(default_namespace_prefixes)

    if onto_ref_folder:
        file_prefixes = iterate_ttl_graphs(onto_ref_folder, read_prefixes_from_graph)
        prefixes |= merge_dictionaries(file_prefixes)
        inv_prefixes = {value: key for key, value in prefixes.items()}

        residual_file_prefixes = iterate_ttl_graphs(
            onto_ref_folder,
            partial(generate_residual_prefixes, inv_prefixes=inv_prefixes),
        )
        residual_file_prefixes = {
            key: value
            for residual_prefixes in residual_file_prefixes
            for key, value in residual_prefixes.items()
        }
        prefixes.update(residual_file_prefixes)
        inv_prefixes = {value: key for key, value in prefixes.items()}

    search_terms = get_search_terms_from_defaults(default_namespace_prefixes)

    if onto_ref_folder:
        file_search_terms = iterate_ttl_graphs(
            onto_ref_folder,
            partial(get_search_terms_from_graph, inv_prefixes=inv_prefixes),
        )
        search_terms |= merge_dictionaries(file_search_terms)

    aliases = {
        term: aliases
        for term, aliases in iter_diagram_terms(
            graph, lambda term: (term, get_term_aliases(term))
        )
    }

    literal_terms = {
        term
        for term in filter(lambda term: ('"' in term), get_diagram_terms_iter(graph))
    }
    constructed_terms = {
        term: term_uri_ref
        for term, term_uri_ref in map(
            lambda term_info: (
                term_info[0],
                construct_term_uri(
                    *get_abbrev_term(term_info[0], term_info[1]), prefixes=prefixes
                ),
            ),
            filter(
                lambda term_info: term_info[0] not in literal_terms,
                get_diagram_terms_iter_with_pred(graph),
            ),
        )
    }
    search_keys = {
        term: search_key
        for term, search_key in iter_diagram_terms(
            graph, lambda term: (term, get_term_search_keys(term, inv_prefixes))
        )
    }
    substitution_results = {
        term: substituted_value
        for term, substituted_value in iter_diagram_terms(
            graph,
            lambda term: (term, substitute_term(search_keys[term], search_terms)),
        )
        if substituted_value is not None
    }

    inv_constructed_terms = {value: key for key, value in constructed_terms.items()}

    constructed_terms.update(substitution_results)
    constructed_literal_terms = {
        term: construct_literal(
            term, lang=get_literal_lang_annotation(term), datatype=get_literal_data_type(term, search_terms)
        )
        for term in literal_terms
    }
    constructed_terms.update(constructed_literal_terms)

    output_graph = nx.DiGraph()
    for subj, obj, data in graph.edges(data=True):
        pred = data["label"]
        subj, obj, pred = tuple(constructed_terms[key] for key in (subj, obj, pred))
        output_graph.add_edge(subj, obj, label=pred)

    class_terms = get_class_terms(output_graph)
    predicate_terms = {data["label"] for _, _, data in output_graph.edges(data=True)}
    literal_terms = set(constructed_literal_terms.values())
    class_terms -= predicate_terms
    all_terms = (output_graph.nodes() | predicate_terms) - literal_terms

    pred_doms_ranges = get_doms_ranges(output_graph)

    # # create the rdf graph to store the ttl output
    rdf_graph = rdflib.Graph()

    # bind prefixes to namespaces for the rdf graph
    rdf_graph = bind_prefixes(rdf_graph, prefixes)

    # add all of the class terms as a type
    for term in class_terms:
        rdf_graph.add((term, RDF.type, OWL.Class))

    # if the term is a predicate and is not part of the default namespaces, add an object property type to the ttl file
    for term in predicate_terms:
        # TODO: Assume all predicates are object properties for now, change later
        if term_not_in_default_namespace(
            term, inv_prefixes, default_namespace_prefixes
        ):
            rdf_graph.add((term, RDF.type, OWL.ObjectProperty))

    term_in_search_results_filter = partial(
        term_in_search_results, inv_prefixes=inv_prefixes, search_terms=search_terms
    )
    term_not_in_default_namespace_filter = partial(
        term_not_in_default_namespace,
        inv_prefixes=inv_prefixes,
        default_namespace_prefixes=default_namespace_prefixes,
    )

    exact_match_property_predicates = [RDF.value, RDFS.label]
    exact_match_properties = {
        term: {prop: value}
        for prop in exact_match_property_predicates
        for result in map(
            lambda rdf_graph, prop=prop: map(
                lambda graph_term: (
                    graph_term,
                    get_term_value(subj=graph_term, pred=prop, ref_rdf_graph=rdf_graph),
                ),
                all_terms,
            ),
            get_ttl_file_iter(onto_ref_folder),
        )
        for term, value in result
    }
    rdf_graph = reduce(
        lambda rdf_graph, graph_term: add_exact_matches(
            term=graph_term,
            match_properties=exact_match_properties[graph_term],
            rdf_graph=rdf_graph,
        ),
        filter(
            term_in_search_results_filter,
            filter(term_not_in_default_namespace_filter, all_terms),
        ),
        rdf_graph,
    )
    rdf_graph = reduce(
        lambda rdf_graph, graph_term: add_labels(
            term=graph_term,
            labels=aliases[inv_constructed_terms[graph_term]],
            rdf_graph=rdf_graph,
        ),
        filter(
            term_not_in_default_namespace_filter,
            filterfalse(term_in_search_results_filter, all_terms),
        ),
        rdf_graph,
    )
    rdf_graph = reduce(
        lambda rdf_graph, graph_term: add_domains_ranges(
            term=graph_term,
            domains_ranges=pred_doms_ranges[graph_term],
            rdf_graph=rdf_graph,
        ),
        filter(
            term_not_in_default_namespace_filter,
            filterfalse(term_in_search_results_filter, predicate_terms),
        ),
        rdf_graph,
    )

    # now add the triples from the drawio diagram
    for domain_term, range_term, data in output_graph.edges(data=True):
        predicate_term = data["label"]
        rdf_graph.add((domain_term, predicate_term, range_term))
    # serialize the output as a turtle file
    rdf_graph.serialize(output_path)
