import rdflib
import pytest
from axiusmem.query_engine import sparql_select, sparql_construct, sparql_update

EX = rdflib.Namespace("http://example.org/")

@pytest.fixture
def sample_graph():
    g = rdflib.Graph()
    g.add((EX.Alice, EX.knows, EX.Bob))
    g.add((EX.Bob, EX.knows, EX.Charlie))
    g.add((EX.Alice, rdflib.RDF.type, EX.Person))
    g.add((EX.Bob, rdflib.RDF.type, EX.Person))
    g.add((EX.Charlie, rdflib.RDF.type, EX.Person))
    return g

def test_sparql_select(sample_graph):
    query = """
    SELECT ?s ?o WHERE {
        ?s <http://example.org/knows> ?o .
    }
    """
    results, df = sparql_select(sample_graph, query)
    assert {"s": EX.Alice, "o": EX.Bob} in results
    assert {"s": EX.Bob, "o": EX.Charlie} in results
    assert len(df) == 2

def test_sparql_construct(sample_graph):
    query = """
    CONSTRUCT { ?a <http://example.org/knows> ?b } WHERE { ?a <http://example.org/knows> ?b }
    """
    g2 = sparql_construct(sample_graph, query)
    assert (EX.Alice, EX.knows, EX.Bob) in g2
    assert (EX.Bob, EX.knows, EX.Charlie) in g2
    assert (EX.Charlie, EX.knows, EX.Bob) not in g2

def test_sparql_update(sample_graph):
    insert_query = """
    INSERT DATA { <http://example.org/Charlie> <http://example.org/knows> <http://example.org/Alice> }
    """
    sparql_update(sample_graph, insert_query)
    assert (EX.Charlie, EX.knows, EX.Alice) in sample_graph
    delete_query = """
    DELETE DATA { <http://example.org/Alice> <http://example.org/knows> <http://example.org/Bob> }
    """
    sparql_update(sample_graph, delete_query)
    assert (EX.Alice, EX.knows, EX.Bob) not in sample_graph 