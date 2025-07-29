"""
Query engine for SPARQL construction and execution in AxiusMEM.

Provides functions to run SPARQL SELECT, CONSTRUCT, and UPDATE queries on rdflib graphs, with results formatted for Pythonic use.
"""
import pandas as pd

def sparql_select(graph, query):
    """
    Run a SPARQL SELECT query on the given graph.

    Args:
        graph (rdflib.Graph): The RDF graph to query.
        query (str): The SPARQL SELECT query string.

    Returns:
        Tuple[List[dict], pandas.DataFrame]: Results as a list of dicts and as a DataFrame.

    Example:
        >>> results, df = sparql_select(graph, 'SELECT ?s ?o WHERE { ?s <http://example.org/knows> ?o . }')
    """
    qres = graph.query(query)
    results = [{str(var): row[var] for var in qres.vars} for row in qres]
    df = pd.DataFrame(results)
    return results, df

def sparql_construct(graph, query):
    """
    Run a SPARQL CONSTRUCT query on the given graph.

    Args:
        graph (rdflib.Graph): The RDF graph to query.
        query (str): The SPARQL CONSTRUCT query string.

    Returns:
        rdflib.Graph: A new graph with the constructed triples.

    Example:
        >>> g2 = sparql_construct(graph, 'CONSTRUCT { ?a <http://example.org/knows> ?b } WHERE { ?a <http://example.org/knows> ?b }')
    """
    g2 = graph.query(query).graph
    return g2

def sparql_update(graph, query):
    """
    Run a SPARQL UPDATE (INSERT/DELETE) query on the given graph.

    Args:
        graph (rdflib.Graph): The RDF graph to update.
        query (str): The SPARQL UPDATE query string.

    Returns:
        None

    Example:
        >>> sparql_update(graph, 'INSERT DATA { <http://example.org/Alice> <http://example.org/knows> <http://example.org/Bob> }')
    """
    graph.update(query) 