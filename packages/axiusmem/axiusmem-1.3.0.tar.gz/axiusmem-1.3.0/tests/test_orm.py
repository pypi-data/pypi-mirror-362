import pytest
import dataclasses
from rdflib import Graph, URIRef
from axiusmem.orm import (
    object_to_rdf,
    rdf_to_object,
    define_entity_type,
    define_relationship_type,
    serialize_object,
    deserialize_object,
    EX
)

@dataclasses.dataclass
class Person:
    name: str
    age: int

def test_object_to_rdf_and_rdf_to_object_with_dataclass():
    """Test mapping a dataclass to RDF and back."""
    g = Graph()
    alice = Person('Alice', 30)
    subj = object_to_rdf(alice, g, class_uri=EX.Person)
    assert subj is not None
    obj = rdf_to_object(g, subj)
    assert obj['name'] == 'Alice'
    assert obj['age'] == '30'
    assert 'rdf_type' in obj

def test_object_to_rdf_and_rdf_to_object_with_dict():
    """Test mapping a dict to RDF and back."""
    g = Graph()
    d = {'foo': 'bar', 'num': 42}
    subj = object_to_rdf(d, g)
    assert subj is not None
    obj = rdf_to_object(g, subj)
    assert obj['foo'] == 'bar'
    assert obj['num'] == '42'

def test_define_entity_type_and_relationship_type():
    """Test defining new entity and relationship types in the ontology."""
    g = Graph()
    class_uri = define_entity_type(g, 'SmartDevice')
    assert (class_uri, None, None) in g
    prop_uri = define_relationship_type(g, 'controls', EX.Agent, EX.Device)
    assert (prop_uri, None, None) in g

def test_serialize_and_deserialize_object():
    """Test serializing and deserializing a Python object to/from RDF."""
    d = {'x': 'y', 'z': 123}
    rdf_str = serialize_object(d, format='turtle')
    assert '@prefix' in rdf_str or 'http://axiusmem.org/example/' in rdf_str
    objs = deserialize_object(rdf_str, format='turtle')
    found = any(obj.get('x') == 'y' and obj.get('z') == '123' for obj in objs)
    assert found

def test_object_to_rdf_invalid_type():
    """Test that object_to_rdf raises ValueError for unsupported types."""
    g = Graph()
    with pytest.raises(ValueError):
        object_to_rdf(42, g) 