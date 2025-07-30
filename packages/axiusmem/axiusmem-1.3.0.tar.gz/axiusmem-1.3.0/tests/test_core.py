import os
import tempfile
import rdflib
import pytest
from axiusmem.core import AxiusMEM

TEST_ONTOLOGY_TTL = """
@prefix ex: <http://example.org/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:Person a owl:Class ; rdfs:label "Person" .
"""

def test_rdf_graph_and_ontology_loading():
    with tempfile.NamedTemporaryFile("w+", suffix=".ttl", delete=False) as f:
        f.write(TEST_ONTOLOGY_TTL)
        f.flush()
        mem = AxiusMEM(ontology_path=f.name)
        g = mem.get_graph()
        assert (rdflib.URIRef("http://example.org/Person"), rdflib.RDF.type, rdflib.OWL.Class) in g
    os.remove(f.name)

def test_define_class_and_property():
    mem = AxiusMEM()
    class_uri = "http://example.org/Animal"
    prop_uri = "http://example.org/hasName"
    c = mem.define_class(class_uri, label="Animal", comment="An animal class")
    p = mem.define_property(prop_uri, domain=class_uri, range_="http://www.w3.org/2001/XMLSchema#string", label="has name")
    g = mem.get_graph()
    assert (c, rdflib.RDF.type, rdflib.OWL.Class) in g
    assert (p, rdflib.RDF.type, rdflib.OWL.ObjectProperty) in g
    assert (p, rdflib.RDFS.domain, c) in g

def test_add_triples_with_provenance(monkeypatch):
    mem = AxiusMEM()
    s = rdflib.URIRef("http://example.org/Alice")
    p = rdflib.URIRef("http://example.org/knows")
    o = rdflib.URIRef("http://example.org/Bob")
    provenance = {"source": "test", "timestamp": "2024-07-01", "agent": "tester"}
    called = {}
    def fake_attach_provenance(triple, **prov):
        called["triple"] = triple
        called["prov"] = prov
    monkeypatch.setattr("axiusmem.core.attach_provenance", fake_attach_provenance)
    mem.add_triples([(s, p, o)], provenance=provenance)
    g = mem.get_graph()
    assert (s, p, o) in g
    assert called["triple"] == (s, p, o)
    assert called["prov"] == provenance 