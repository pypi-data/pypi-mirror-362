"""
Utilities for AI agent context and memory management in AxiusMEM.

These helpers support context retrieval, agent memory storage, retrieval, formatting for LLM prompt consumption, and dynamic ontology updates.
"""
import logging
from typing import Any, List, Dict, Optional
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, DCTERMS

AGENT = Namespace("http://axiusmem.org/agent/")
MEM = Namespace("http://axiusmem.org/memory/")


def get_context_for_agent(graph: Graph, agent_id: str, context_type: Optional[str] = None, time: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve relevant context for an agent from the knowledge graph.

    Args:
        graph (rdflib.Graph): The RDF graph.
        agent_id (str): The agent's unique identifier.
        context_type (Optional[str]): Type of context to retrieve (e.g., 'profile', 'history').
        time (Optional[str]): Point in time or interval for temporal context.

    Returns:
        List[Dict[str, Any]]: List of context facts (subject, predicate, object, [timestamp]).

    Example:
        >>> context = get_context_for_agent(graph, 'agent-001', context_type='profile')
    """
    agent_uri = URIRef(AGENT[agent_id])
    results = []
    for s, p, o in graph.triples((agent_uri, None, None)):
        fact = {'subject': str(s), 'predicate': str(p), 'object': str(o)}
        # Optionally filter by context_type or time
        results.append(fact)
    return results


def store_agent_memory(graph: Graph, agent_id: str, memory: Dict[str, Any], provenance: Optional[Dict[str, Any]] = None) -> URIRef:
    """
    Store agent-specific memory in the knowledge graph.

    Args:
        graph (rdflib.Graph): The RDF graph.
        agent_id (str): The agent's unique identifier.
        memory (Dict[str, Any]): The memory or experience to store (as a dict).
        provenance (Optional[Dict[str, Any]]): Provenance metadata (e.g., source, timestamp).

    Returns:
        URIRef: The URI of the stored memory node.

    Example:
        >>> store_agent_memory(graph, 'agent-001', {'event': 'login', 'timestamp': '2024-07-01'})
    """
    agent_uri = URIRef(AGENT[agent_id])
    mem_uri = URIRef(MEM[f"{agent_id}_mem_{hash(str(memory))}"])
    graph.add((agent_uri, MEM.hasMemory, mem_uri))
    for k, v in memory.items():
        graph.add((mem_uri, MEM[k], Literal(v)))
    if provenance:
        for pk, pv in provenance.items():
            graph.add((mem_uri, DCTERMS[pk], Literal(pv)))
    return mem_uri


def retrieve_agent_memories(graph: Graph, agent_id: str) -> List[Dict[str, Any]]:
    """
    Retrieve all memories for a given agent from the knowledge graph.

    Args:
        graph (rdflib.Graph): The RDF graph.
        agent_id (str): The agent's unique identifier.

    Returns:
        List[Dict[str, Any]]: List of memory dicts.

    Example:
        >>> memories = retrieve_agent_memories(graph, 'agent-001')
    """
    agent_uri = URIRef(AGENT[agent_id])
    memories = []
    for _, _, mem_uri in graph.triples((agent_uri, MEM.hasMemory, None)):
        mem_dict = {'uri': str(mem_uri)}
        for _, p, o in graph.triples((mem_uri, None, None)):
            if p.startswith(str(MEM)):
                mem_dict[str(p).replace(str(MEM), '')] = str(o)
            elif p.startswith(str(DCTERMS)):
                mem_dict[str(p).replace(str(DCTERMS), 'prov_')] = str(o)
        memories.append(mem_dict)
    return memories


def format_context_for_llm(context: List[Dict[str, Any]], format: str = 'text') -> str:
    """
    Format context data for LLM prompt consumption.

    Args:
        context (List[Dict[str, Any]]): List of context facts or memories.
        format (str): Output format ('text', 'json').

    Returns:
        str: Formatted string suitable for LLM input.

    Example:
        >>> prompt = format_context_for_llm(context, format='text')
    """
    import json
    if format == 'json':
        return json.dumps(context, indent=2)
    # Default: human-readable text
    lines = []
    for fact in context:
        line = ', '.join(f"{k}: {v}" for k, v in fact.items())
        lines.append(line)
    return '\n'.join(lines)


def propose_ontology_update(graph: Graph, agent_id: str, new_concept_or_relation: Dict[str, Any]) -> bool:
    """
    Allow an agent to propose a new concept or relationship to the ontology.

    Args:
        graph (rdflib.Graph): The RDF graph.
        agent_id (str): The agent's unique identifier.
        new_concept_or_relation (Dict[str, Any]): Description of the new class/property/relation.

    Returns:
        bool: True if proposal accepted (stub: always True for now).

    Example:
        >>> propose_ontology_update(graph, 'agent-001', {'type': 'Class', 'name': 'SmartDevice'})
    """
    # Stub: In production, validate and extend ontology safely
    logging.info(f"Agent {agent_id} proposes ontology update: {new_concept_or_relation}")
    return True 