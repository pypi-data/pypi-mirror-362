"""
General utilities for AxiusMEM.

Includes data validation against ontology and provenance attachment helpers.
"""

def validate_data_against_ontology(graph, data):
    """
    Validate triples against the loaded ontology in the graph.

    Checks:
      - Predicate is defined as a property in the ontology
      - (If possible) Subject and object match expected domain/range

    Args:
        graph (rdflib.Graph): The RDF graph with ontology loaded.
        data (list): List of (subject, predicate, object) triples to validate.

    Returns:
        list: List of error strings (empty if valid).

    Example:
        >>> errors = validate_data_against_ontology(graph, [(s, p, o)])
    """
    errors = []
    # Get all known properties from the ontology
    known_properties = set(graph.subjects(rdflib.RDF.type, rdflib.OWL.ObjectProperty))
    known_properties |= set(graph.subjects(rdflib.RDF.type, rdflib.OWL.DatatypeProperty))
    # Get domain/range info
    domain_map = {p: graph.value(p, rdflib.RDFS.domain) for p in known_properties}
    range_map = {p: graph.value(p, rdflib.RDFS.range) for p in known_properties}
    for s, p, o in data:
        if p not in known_properties:
            errors.append(f"Predicate {p} is not defined in ontology.")
        else:
            domain = domain_map.get(p)
            if domain:
                # Check if subject is an instance of the domain class
                if (s, rdflib.RDF.type, domain) not in graph:
                    errors.append(f"Subject {s} is not an instance of domain {domain} for property {p}.")
            range_ = range_map.get(p)
            if range_:
                # Check if object is an instance of the range class (if object is a URI)
                if isinstance(o, rdflib.URIRef) and (o, rdflib.RDF.type, range_) not in graph:
                    errors.append(f"Object {o} is not an instance of range {range_} for property {p}.")
    return errors

def attach_provenance(triple, source, timestamp, agent):
    """
    Attach provenance info to a triple (placeholder).

    Args:
        triple (tuple): The (subject, predicate, object) triple.
        source (str): Source of the data.
        timestamp (str): Timestamp of ingestion.
        agent (str): Agent responsible for the data.

    Returns:
        None

    Example:
        >>> attach_provenance((s, p, o), source='api', timestamp='2024-07-01', agent='agent-001')
    """
    # Placeholder: attach provenance info to a triple
    pass 