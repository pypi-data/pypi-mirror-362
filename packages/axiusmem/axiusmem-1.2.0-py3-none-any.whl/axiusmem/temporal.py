"""
Temporal logic helpers for bi-temporal data model in AxiusMEM.

This module provides functions to attach and query valid time and transaction time for RDF triples,
supporting point-in-time, as-of, and interval-based temporal reasoning.
"""
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, Namespace
from typing import Optional, Tuple

# Namespaces
DCTERMS = Namespace("http://purl.org/dc/terms/")
AXM = Namespace("http://axiusmem.org/ontology#")  # Custom for valid time

def add_valid_time(graph: Graph, triple: Tuple, valid_from: str, valid_to: Optional[str] = None) -> BNode:
    """
    Attach valid time interval to a triple using RDF reification and custom properties.

    Args:
        graph (Graph): The RDF graph.
        triple (Tuple): The (subject, predicate, object) triple.
        valid_from (str): Start of valid time (ISO 8601 string).
        valid_to (Optional[str]): End of valid time (ISO 8601 string), or None for open-ended.

    Returns:
        BNode: The reification node for the triple.

    Example:
        >>> add_valid_time(graph, (s, p, o), "2024-01-01", "2024-12-31")
    """
    s, p, o = triple
    stmt = BNode()
    graph.add((stmt, RDF.type, RDF.Statement))
    graph.add((stmt, RDF.subject, s))
    graph.add((stmt, RDF.predicate, p))
    graph.add((stmt, RDF.object, o))
    graph.add((stmt, AXM.validFrom, Literal(valid_from)))
    if valid_to:
        graph.add((stmt, AXM.validTo, Literal(valid_to)))
    return stmt

def add_transaction_time(graph: Graph, triple: Tuple, transaction_from: str, transaction_to: Optional[str] = None) -> BNode:
    """
    Attach transaction time interval to a triple using RDF reification and dcterms properties.

    Args:
        graph (Graph): The RDF graph.
        triple (Tuple): The (subject, predicate, object) triple.
        transaction_from (str): Start of transaction time (ISO 8601 string).
        transaction_to (Optional[str]): End of transaction time (ISO 8601 string), or None for open-ended.

    Returns:
        BNode: The reification node for the triple.

    Example:
        >>> add_transaction_time(graph, (s, p, o), "2024-01-01")
    """
    s, p, o = triple
    stmt = BNode()
    graph.add((stmt, RDF.type, RDF.Statement))
    graph.add((stmt, RDF.subject, s))
    graph.add((stmt, RDF.predicate, p))
    graph.add((stmt, RDF.object, o))
    graph.add((stmt, DCTERMS.created, Literal(transaction_from)))
    if transaction_to:
        graph.add((stmt, DCTERMS.modified, Literal(transaction_to)))
    return stmt

def query_point_in_time(graph: Graph, time: str) -> Graph:
    """
    Return a subgraph of triples valid at a specific valid time.

    Args:
        graph (Graph): The RDF graph.
        time (str): The valid time (ISO 8601 string).

    Returns:
        Graph: Subgraph of triples valid at the given time.
    """
    result = Graph()
    for stmt in graph.subjects(RDF.type, RDF.Statement):
        valid_from = graph.value(stmt, AXM.validFrom)
        valid_to = graph.value(stmt, AXM.validTo)
        if valid_from and valid_from <= Literal(time):
            if not valid_to or Literal(time) <= valid_to:
                s = graph.value(stmt, RDF.subject)
                p = graph.value(stmt, RDF.predicate)
                o = graph.value(stmt, RDF.object)
                result.add((s, p, o))
    return result

def query_as_of(graph: Graph, transaction_time: str) -> Graph:
    """
    Return a subgraph of triples as known at a specific transaction time.

    Args:
        graph (Graph): The RDF graph.
        transaction_time (str): The transaction time (ISO 8601 string).

    Returns:
        Graph: Subgraph of triples as known at the given transaction time.
    """
    result = Graph()
    for stmt in graph.subjects(RDF.type, RDF.Statement):
        created = graph.value(stmt, DCTERMS.created)
        modified = graph.value(stmt, DCTERMS.modified)
        if created and created <= Literal(transaction_time):
            if not modified or Literal(transaction_time) <= modified:
                s = graph.value(stmt, RDF.subject)
                p = graph.value(stmt, RDF.predicate)
                o = graph.value(stmt, RDF.object)
                result.add((s, p, o))
    return result

def query_interval_valid_time(graph: Graph, start: str, end: str) -> Graph:
    """
    Return a subgraph of triples valid at any point during [start, end].

    Args:
        graph (Graph): The RDF graph.
        start (str): Interval start (ISO 8601 string).
        end (str): Interval end (ISO 8601 string).

    Returns:
        Graph: Subgraph of triples valid at any point during the interval.
    """
    result = Graph()
    for stmt in graph.subjects(RDF.type, RDF.Statement):
        valid_from = graph.value(stmt, AXM.validFrom)
        valid_to = graph.value(stmt, AXM.validTo)
        # Overlap if (valid_from <= end) and (valid_to is None or valid_to >= start)
        if valid_from and valid_from <= Literal(end):
            if not valid_to or valid_to >= Literal(start):
                s = graph.value(stmt, RDF.subject)
                p = graph.value(stmt, RDF.predicate)
                o = graph.value(stmt, RDF.object)
                result.add((s, p, o))
    return result

def query_interval_transaction_time(graph: Graph, start: str, end: str) -> Graph:
    """
    Return a subgraph of triples known at any point during [start, end].

    Args:
        graph (Graph): The RDF graph.
        start (str): Interval start (ISO 8601 string).
        end (str): Interval end (ISO 8601 string).

    Returns:
        Graph: Subgraph of triples known at any point during the interval.
    """
    result = Graph()
    for stmt in graph.subjects(RDF.type, RDF.Statement):
        created = graph.value(stmt, DCTERMS.created)
        modified = graph.value(stmt, DCTERMS.modified)
        # Overlap if (created <= end) and (modified is None or modified >= start)
        if created and created <= Literal(end):
            if not modified or modified >= Literal(start):
                s = graph.value(stmt, RDF.subject)
                p = graph.value(stmt, RDF.predicate)
                o = graph.value(stmt, RDF.object)
                result.add((s, p, o))
    return result 