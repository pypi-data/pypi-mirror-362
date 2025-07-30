import pytest
from rdflib import Graph
from axiusmem.agent_utils import (
    get_context_for_agent,
    store_agent_memory,
    retrieve_agent_memories,
    format_context_for_llm,
    propose_ontology_update,
)

def test_store_and_retrieve_agent_memory():
    """Test storing and retrieving agent memories."""
    g = Graph()
    agent_id = 'agent-001'
    memory = {'event': 'login', 'timestamp': '2024-07-01'}
    mem_uri = store_agent_memory(g, agent_id, memory)
    assert mem_uri is not None
    memories = retrieve_agent_memories(g, agent_id)
    assert len(memories) == 1
    assert memories[0]['event'] == 'login'
    assert memories[0]['timestamp'] == '2024-07-01'

def test_get_context_for_agent():
    """Test context retrieval for an agent."""
    g = Graph()
    agent_id = 'agent-002'
    # Add some triples
    store_agent_memory(g, agent_id, {'event': 'purchase', 'item': 'book'})
    context = get_context_for_agent(g, agent_id)
    assert isinstance(context, list)
    assert any('object' in fact for fact in context)

def test_format_context_for_llm_text_and_json():
    """Test formatting context for LLM in text and JSON formats."""
    context = [
        {'subject': 'a', 'predicate': 'b', 'object': 'c'},
        {'subject': 'x', 'predicate': 'y', 'object': 'z'}
    ]
    text = format_context_for_llm(context, format='text')
    assert 'subject: a' in text
    json_str = format_context_for_llm(context, format='json')
    assert '"subject": "a"' in json_str

def test_propose_ontology_update_logs_and_returns_true(caplog):
    """Test ontology update proposal logs and returns True."""
    g = Graph()
    agent_id = 'agent-003'
    proposal = {'type': 'Class', 'name': 'SmartDevice'}
    with caplog.at_level('INFO'):
        result = propose_ontology_update(g, agent_id, proposal)
    assert result is True
    assert any('proposes ontology update' in m for m in caplog.text.splitlines())

def test_store_agent_memory_with_provenance():
    """Test storing agent memory with provenance metadata."""
    g = Graph()
    agent_id = 'agent-004'
    memory = {'event': 'logout'}
    provenance = {'created': '2024-07-02', 'source': 'test'}
    mem_uri = store_agent_memory(g, agent_id, memory, provenance=provenance)
    memories = retrieve_agent_memories(g, agent_id)
    assert len(memories) == 1
    assert memories[0]['event'] == 'logout'
    assert memories[0]['prov_created'] == '2024-07-02'
    assert memories[0]['prov_source'] == 'test' 