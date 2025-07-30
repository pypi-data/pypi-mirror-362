import rdflib
import pytest
from axiusmem.core import AxiusMEM

EX = rdflib.Namespace("http://example.org/")

def test_add_triples_with_temporal_and_provenance(monkeypatch):
    mem = AxiusMEM()
    triple = (EX.Alice, EX.knows, EX.Bob)
    provenance = {"source": "test", "timestamp": "2024-07-01", "agent": "tester"}
    called = {}
    def fake_attach_provenance(triple, **prov):
        called["triple"] = triple
        called["prov"] = prov
    monkeypatch.setattr("axiusmem.core.attach_provenance", fake_attach_provenance)
    mem.add_triples([triple], valid_time={"from": "2024-01-01", "to": "2024-12-31"}, transaction_time={"from": "2024-01-01"}, provenance=provenance)
    g = mem.get_graph()
    assert (EX.Alice, EX.knows, EX.Bob) in g
    assert called["triple"] == triple
    assert called["prov"] == provenance

def test_update_triple(monkeypatch):
    mem = AxiusMEM()
    old_triple = (EX.Alice, EX.knows, EX.Bob)
    new_triple = (EX.Alice, EX.knows, EX.Charlie)
    mem.add_triples([old_triple])
    mem.update_triple(old_triple, new_triple, valid_time={"from": "2024-01-01"})
    g = mem.get_graph()
    assert (EX.Alice, EX.knows, EX.Bob) not in g
    assert (EX.Alice, EX.knows, EX.Charlie) in g

def test_delete_triple(monkeypatch):
    mem = AxiusMEM()
    triple = (EX.Alice, EX.knows, EX.Bob)
    mem.add_triples([triple])
    mem.delete_triple(triple, transaction_time={"from": "2024-06-01"})
    g = mem.get_graph()
    assert (EX.Alice, EX.knows, EX.Bob) not in g 