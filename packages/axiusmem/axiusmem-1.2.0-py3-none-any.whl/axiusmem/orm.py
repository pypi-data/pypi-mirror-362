"""
ORM-like utilities for mapping Python objects to RDF and vice versa in AxiusMEM.

These helpers enable conversion between Python objects and RDF triples for easier integration with the knowledge graph.
"""
from typing import Any, Dict, List, Optional, Type
from rdflib import Graph, URIRef, BNode, Literal, Namespace, RDF, RDFS
import dataclasses
import json

EX = Namespace("http://axiusmem.org/example/")


def object_to_rdf(obj: Any, graph: Graph, class_uri: Optional[URIRef] = None, subject_uri: Optional[URIRef] = None) -> URIRef:
    """
    Map a Python dataclass or dict to RDF triples in the given graph.

    Args:
        obj (Any): The Python object (dataclass or dict) to map.
        graph (rdflib.Graph): The RDF graph to add triples to.
        class_uri (Optional[URIRef]): RDF class URI for the object.
        subject_uri (Optional[URIRef]): Optionally specify the subject URI.

    Returns:
        URIRef: The subject URI of the created RDF resource.

    Example:
        >>> @dataclasses.dataclass
        ... class Person:
        ...     name: str
        ...     age: int
        >>> g = Graph()
        >>> s = object_to_rdf(Person('Alice', 30), g, class_uri=EX.Person)
    """
    if subject_uri is None:
        subject = BNode()
    else:
        subject = subject_uri
    if class_uri:
        graph.add((subject, RDF.type, class_uri))
    if dataclasses.is_dataclass(obj):
        fields = dataclasses.asdict(obj)
    elif isinstance(obj, dict):
        fields = obj
    else:
        raise ValueError("Only dataclasses or dicts are supported.")
    for k, v in fields.items():
        pred = EX[k]
        graph.add((subject, pred, Literal(v)))
    return subject


def rdf_to_object(graph: Graph, subject: URIRef, as_dict: bool = True) -> Any:
    """
    Map an RDF resource to a Python dict (or dataclass in future).

    Args:
        graph (rdflib.Graph): The RDF graph.
        subject (rdflib.URIRef): The RDF resource to map.
        as_dict (bool): If True, return a dict; otherwise, return a dataclass (future).

    Returns:
        dict: The corresponding Python dict.

    Example:
        >>> obj = rdf_to_object(g, s)
    """
    result = {}
    for _, p, o in graph.triples((subject, None, None)):
        if p == RDF.type:
            result['rdf_type'] = str(o)
        else:
            result[str(p).replace(str(EX), '')] = str(o)
    return result


def define_entity_type(graph: Graph, class_name: str, base_class_uri: Optional[URIRef] = None) -> URIRef:
    """
    Define a new RDF class (entity type) in the ontology.

    Args:
        graph (rdflib.Graph): The RDF graph.
        class_name (str): Name of the new class.
        base_class_uri (Optional[URIRef]): Optional base class URI.

    Returns:
        URIRef: The URI of the new class.

    Example:
        >>> define_entity_type(g, 'SmartDevice')
    """
    class_uri = EX[class_name]
    graph.add((class_uri, RDF.type, RDFS.Class))
    if base_class_uri:
        graph.add((class_uri, RDFS.subClassOf, base_class_uri))
    return class_uri


def define_relationship_type(graph: Graph, property_name: str, domain_uri: URIRef, range_uri: URIRef) -> URIRef:
    """
    Define a new RDF property (relationship type) in the ontology.

    Args:
        graph (rdflib.Graph): The RDF graph.
        property_name (str): Name of the property.
        domain_uri (URIRef): Domain class URI.
        range_uri (URIRef): Range class URI.

    Returns:
        URIRef: The URI of the new property.

    Example:
        >>> define_relationship_type(g, 'controls', EX.Agent, EX.Device)
    """
    prop_uri = EX[property_name]
    graph.add((prop_uri, RDF.type, RDF.Property))
    graph.add((prop_uri, RDFS.domain, domain_uri))
    graph.add((prop_uri, RDFS.range, range_uri))
    return prop_uri


def serialize_object(obj: Any, format: str = 'turtle') -> str:
    """
    Serialize a Python object (dataclass or dict) to RDF in the given format.

    Args:
        obj (Any): The Python object to serialize.
        format (str): RDF serialization format ('turtle', 'nt', etc.).

    Returns:
        str: RDF data as a string.

    Example:
        >>> serialize_object({'name': 'Alice', 'age': 30}, format='turtle')
    """
    g = Graph()
    object_to_rdf(obj, g)
    return g.serialize(format=format).decode() if hasattr(g.serialize(format=format), 'decode') else g.serialize(format=format)


def deserialize_object(rdf_data: str, format: str = 'turtle') -> List[Dict[str, Any]]:
    """
    Deserialize RDF data to a list of Python dicts.

    Args:
        rdf_data (str): RDF data as a string.
        format (str): RDF serialization format ('turtle', 'nt', etc.).

    Returns:
        List[Dict[str, Any]]: List of Python dicts representing resources.

    Example:
        >>> deserialize_object(rdf_str, format='turtle')
    """
    g = Graph()
    g.parse(data=rdf_data, format=format)
    results = []
    for s in set(g.subjects()):
        results.append(rdf_to_object(g, s))
    return results 