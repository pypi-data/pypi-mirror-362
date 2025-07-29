import rdflib
import pytest
from axiusmem.core import AxiusMEM

EX = rdflib.Namespace("http://example.org/")

@pytest.fixture
def mem_with_data():
    mem = AxiusMEM()
    mem.add_triples([
        (EX.Alice, EX.knows, EX.Bob),
        (EX.Bob, EX.knows, EX.Charlie),
        (EX.Alice, rdflib.RDF.type, EX.Person),
        (EX.Bob, rdflib.RDF.type, EX.Person),
        (EX.Charlie, rdflib.RDF.type, EX.Person),
    ])
    return mem

def test_select(mem_with_data):
    query = """
    SELECT ?s ?o WHERE {
        ?s <http://example.org/knows> ?o .
    }
    """
    results, df = mem_with_data.select(query)
    assert {"s": EX.Alice, "o": EX.Bob} in results
    assert {"s": EX.Bob, "o": EX.Charlie} in results
    assert len(df) == 2

def test_construct(mem_with_data):
    query = """
    CONSTRUCT { ?a <http://example.org/knows> ?b } WHERE { ?a <http://example.org/knows> ?b }
    """
    g2 = mem_with_data.construct(query)
    assert (EX.Alice, EX.knows, EX.Bob) in g2
    assert (EX.Bob, EX.knows, EX.Charlie) in g2
    assert (EX.Charlie, EX.knows, EX.Bob) not in g2

def test_update(mem_with_data):
    insert_query = """
    INSERT DATA { <http://example.org/Charlie> <http://example.org/knows> <http://example.org/Alice> }
    """
    mem_with_data.update(insert_query)
    g = mem_with_data.get_graph()
    assert (EX.Charlie, EX.knows, EX.Alice) in g
    delete_query = """
    DELETE DATA { <http://example.org/Alice> <http://example.org/knows> <http://example.org/Bob> }
    """
    mem_with_data.update(delete_query)
    assert (EX.Alice, EX.knows, EX.Bob) not in g 

def test_select_point_in_time():
    mem = AxiusMEM()
    EX = rdflib.Namespace("http://example.org/")
    triple = (EX.Alice, EX.knows, EX.Bob)
    mem.add_triples([triple], valid_time={"from": "2024-01-01", "to": "2024-12-31"})
    query = "SELECT ?s ?o WHERE { ?s <http://example.org/knows> ?o . }"
    # Should find triple within interval
    results, df = mem.select_point_in_time(query, "2024-06-01")
    assert {"s": EX.Alice, "o": EX.Bob} in results
    # Should not find triple before interval
    results, df = mem.select_point_in_time(query, "2023-12-31")
    assert {"s": EX.Alice, "o": EX.Bob} not in results
    # Should not find triple after interval
    results, df = mem.select_point_in_time(query, "2025-01-01")
    assert {"s": EX.Alice, "o": EX.Bob} not in results

def test_select_as_of():
    mem = AxiusMEM()
    EX = rdflib.Namespace("http://example.org/")
    triple = (EX.Alice, EX.knows, EX.Bob)
    mem.add_triples([triple], transaction_time={"from": "2024-01-01", "to": "2024-12-31"})
    query = "SELECT ?s ?o WHERE { ?s <http://example.org/knows> ?o . }"
    # Should find triple within interval
    results, df = mem.select_as_of(query, "2024-06-01")
    assert {"s": EX.Alice, "o": EX.Bob} in results
    # Should not find triple before interval
    results, df = mem.select_as_of(query, "2023-12-31")
    assert {"s": EX.Alice, "o": EX.Bob} not in results
    # Should not find triple after interval
    results, df = mem.select_as_of(query, "2025-01-01")
    assert {"s": EX.Alice, "o": EX.Bob} not in results 

def test_select_interval_valid_time():
    mem = AxiusMEM()
    EX = rdflib.Namespace("http://example.org/")
    triple1 = (EX.Alice, EX.knows, EX.Bob)
    triple2 = (EX.Bob, EX.knows, EX.Charlie)
    mem.add_triples([triple1], valid_time={"from": "2024-01-01", "to": "2024-06-30"})
    mem.add_triples([triple2], valid_time={"from": "2024-07-01", "to": "2024-12-31"})
    query = "SELECT ?s ?o WHERE { ?s <http://example.org/knows> ?o . }"
    # Interval overlaps only triple1
    results, df = mem.select_interval_valid_time(query, "2024-01-01", "2024-06-30")
    assert {"s": EX.Alice, "o": EX.Bob} in results
    assert {"s": EX.Bob, "o": EX.Charlie} not in results
    # Interval overlaps only triple2
    results, df = mem.select_interval_valid_time(query, "2024-07-01", "2024-12-31")
    assert {"s": EX.Bob, "o": EX.Charlie} in results
    assert {"s": EX.Alice, "o": EX.Bob} not in results
    # Interval overlaps both
    results, df = mem.select_interval_valid_time(query, "2024-06-01", "2024-07-15")
    assert {"s": EX.Alice, "o": EX.Bob} in results
    assert {"s": EX.Bob, "o": EX.Charlie} in results

def test_select_interval_transaction_time():
    mem = AxiusMEM()
    EX = rdflib.Namespace("http://example.org/")
    triple1 = (EX.Alice, EX.knows, EX.Bob)
    triple2 = (EX.Bob, EX.knows, EX.Charlie)
    mem.add_triples([triple1], transaction_time={"from": "2024-01-01", "to": "2024-06-30"})
    mem.add_triples([triple2], transaction_time={"from": "2024-07-01", "to": "2024-12-31"})
    query = "SELECT ?s ?o WHERE { ?s <http://example.org/knows> ?o . }"
    # Interval overlaps only triple1
    results, df = mem.select_interval_transaction_time(query, "2024-01-01", "2024-06-30")
    assert {"s": EX.Alice, "o": EX.Bob} in results
    assert {"s": EX.Bob, "o": EX.Charlie} not in results
    # Interval overlaps only triple2
    results, df = mem.select_interval_transaction_time(query, "2024-07-01", "2024-12-31")
    assert {"s": EX.Bob, "o": EX.Charlie} in results
    assert {"s": EX.Alice, "o": EX.Bob} not in results
    # Interval overlaps both
    results, df = mem.select_interval_transaction_time(query, "2024-06-01", "2024-07-15")
    assert {"s": EX.Alice, "o": EX.Bob} in results
    assert {"s": EX.Bob, "o": EX.Charlie} in results 

def test_path_query_point_in_time():
    mem = AxiusMEM()
    EX = rdflib.Namespace("http://example.org/")
    mem.add_triples([(EX.Alice, EX.knows, EX.Bob)], valid_time={"from": "2024-01-01", "to": "2024-12-31"})
    mem.add_triples([(EX.Bob, EX.knows, EX.Charlie)], valid_time={"from": "2024-01-01", "to": "2024-12-31"})
    query = "SELECT ?start ?end WHERE { ?start (<http://example.org/knows>)+ ?end . }"
    results, df = mem.path_query_point_in_time(query, "2024-06-01")
    assert {"start": EX.Alice, "end": EX.Bob} in results
    assert {"start": EX.Bob, "end": EX.Charlie} in results
    assert {"start": EX.Alice, "end": EX.Charlie} in results  # Alice->Bob->Charlie

def test_path_query_interval_valid_time():
    mem = AxiusMEM()
    EX = rdflib.Namespace("http://example.org/")
    mem.add_triples([(EX.Alice, EX.knows, EX.Bob)], valid_time={"from": "2024-01-01", "to": "2024-06-30"})
    mem.add_triples([(EX.Bob, EX.knows, EX.Charlie)], valid_time={"from": "2024-07-01", "to": "2024-12-31"})
    query = "SELECT ?start ?end WHERE { ?start (<http://example.org/knows>)+ ?end . }"
    # Only Alice->Bob path in first interval
    results, df = mem.path_query_interval_valid_time(query, "2024-01-01", "2024-06-30")
    assert {"start": EX.Alice, "end": EX.Bob} in results
    assert {"start": EX.Bob, "end": EX.Charlie} not in results
    # Only Bob->Charlie path in second interval
    results, df = mem.path_query_interval_valid_time(query, "2024-07-01", "2024-12-31")
    assert {"start": EX.Bob, "end": EX.Charlie} in results
    assert {"start": EX.Alice, "end": EX.Bob} not in results
    # Both paths in overlapping interval
    results, df = mem.path_query_interval_valid_time(query, "2024-06-01", "2024-07-15")
    assert {"start": EX.Alice, "end": EX.Bob} in results
    assert {"start": EX.Bob, "end": EX.Charlie} in results

def test_aggregate_point_in_time():
    mem = AxiusMEM()
    EX = rdflib.Namespace("http://example.org/")
    mem.add_triples([(EX.Alice, EX.knows, EX.Bob)], valid_time={"from": "2024-01-01", "to": "2024-12-31"})
    mem.add_triples([(EX.Bob, EX.knows, EX.Charlie)], valid_time={"from": "2024-01-01", "to": "2024-12-31"})
    query = "SELECT (COUNT(?s) AS ?count) WHERE { ?s <http://example.org/knows> ?o . }"
    results, df = mem.aggregate_point_in_time(query, "2024-06-01")
    assert results[0]["count"].toPython() == 2

def test_aggregate_interval_valid_time():
    mem = AxiusMEM()
    EX = rdflib.Namespace("http://example.org/")
    mem.add_triples([(EX.Alice, EX.knows, EX.Bob)], valid_time={"from": "2024-01-01", "to": "2024-06-30"})
    mem.add_triples([(EX.Bob, EX.knows, EX.Charlie)], valid_time={"from": "2024-07-01", "to": "2024-12-31"})
    query = "SELECT (COUNT(?s) AS ?count) WHERE { ?s <http://example.org/knows> ?o . }"
    # Only one triple in first interval
    results, df = mem.aggregate_interval_valid_time(query, "2024-01-01", "2024-06-30")
    assert results[0]["count"].toPython() == 1
    # Only one triple in second interval
    results, df = mem.aggregate_interval_valid_time(query, "2024-07-01", "2024-12-31")
    assert results[0]["count"].toPython() == 1
    # Both triples in overlapping interval
    results, df = mem.aggregate_interval_valid_time(query, "2024-06-01", "2024-07-15")
    assert results[0]["count"].toPython() == 2 