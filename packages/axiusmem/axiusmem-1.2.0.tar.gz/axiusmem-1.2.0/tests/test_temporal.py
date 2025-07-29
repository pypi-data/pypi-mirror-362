import rdflib
import pytest
from axiusmem.temporal import add_valid_time, add_transaction_time, query_point_in_time, query_as_of

EX = rdflib.Namespace("http://example.org/")

def test_add_valid_time_and_query():
    g = rdflib.Graph()
    triple = (EX.Alice, EX.knows, EX.Bob)
    add_valid_time(g, triple, valid_from="2024-01-01", valid_to="2024-12-31")
    # Should retrieve triple for a date within the interval
    result = query_point_in_time(g, "2024-06-01")
    assert (EX.Alice, EX.knows, EX.Bob) in result
    # Should not retrieve triple for a date before the interval
    result = query_point_in_time(g, "2023-12-31")
    assert (EX.Alice, EX.knows, EX.Bob) not in result
    # Should not retrieve triple for a date after the interval
    result = query_point_in_time(g, "2025-01-01")
    assert (EX.Alice, EX.knows, EX.Bob) not in result

def test_add_transaction_time_and_query():
    g = rdflib.Graph()
    triple = (EX.Alice, EX.knows, EX.Bob)
    add_transaction_time(g, triple, transaction_from="2024-01-01", transaction_to="2024-12-31")
    # Should retrieve triple for a transaction time within the interval
    result = query_as_of(g, "2024-06-01")
    assert (EX.Alice, EX.knows, EX.Bob) in result
    # Should not retrieve triple for a transaction time before the interval
    result = query_as_of(g, "2023-12-31")
    assert (EX.Alice, EX.knows, EX.Bob) not in result
    # Should not retrieve triple for a transaction time after the interval
    result = query_as_of(g, "2025-01-01")
    assert (EX.Alice, EX.knows, EX.Bob) not in result

def test_valid_time_open_interval():
    g = rdflib.Graph()
    triple = (EX.Alice, EX.knows, EX.Bob)
    add_valid_time(g, triple, valid_from="2024-01-01")
    # Should retrieve triple for any date after valid_from
    assert (EX.Alice, EX.knows, EX.Bob) in query_point_in_time(g, "2024-06-01")
    assert (EX.Alice, EX.knows, EX.Bob) in query_point_in_time(g, "2025-01-01")
    # Should not retrieve triple for a date before valid_from
    assert (EX.Alice, EX.knows, EX.Bob) not in query_point_in_time(g, "2023-12-31")

def test_transaction_time_open_interval():
    g = rdflib.Graph()
    triple = (EX.Alice, EX.knows, EX.Bob)
    add_transaction_time(g, triple, transaction_from="2024-01-01")
    # Should retrieve triple for any transaction time after transaction_from
    assert (EX.Alice, EX.knows, EX.Bob) in query_as_of(g, "2024-06-01")
    assert (EX.Alice, EX.knows, EX.Bob) in query_as_of(g, "2025-01-01")
    # Should not retrieve triple for a transaction time before transaction_from
    assert (EX.Alice, EX.knows, EX.Bob) not in query_as_of(g, "2023-12-31") 