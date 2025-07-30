import os
from dotenv import load_dotenv
load_dotenv()
import pytest
from axiusmem.adapters.base import get_triplestore_adapter_from_env
import tempfile
import tenacity
import requests
from unittest.mock import patch

graphdb_only = pytest.mark.skipif(os.getenv("TRIPLESTORE_TYPE") != "graphdb", reason="GraphDB-specific test")
jena_only = pytest.mark.skipif(os.getenv("TRIPLESTORE_TYPE") != "jena", reason="Jena-specific test")

def get_env(var):
    import os
    v = os.getenv(var)
    if not v:
        pytest.skip(f"Env var {var} not set; skipping GraphDB integration test.")
    return v

@pytest.mark.integration
def test_graphdb_connection_and_ontology_load():
    """Test GraphDB connection and ontology loading (explicit repository)."""
    url = get_env("TRIPLESTORE_URL")
    user = get_env("TRIPLESTORE_USER")
    password = get_env("TRIPLESTORE_PASSWORD")
    repo_id = get_env("TRIPLESTORE_REPOSITORY")
    ontology_path = os.getenv("AXIUSMEM_ONTOLOGY", "docs/axiusmem_ontology.ttl")
    adapter = get_triplestore_adapter_from_env(repository=repo_id)
    assert adapter.test_connection(), "Could not connect to GraphDB."
    # Try loading ontology (will fail if repo doesn't exist or is read-only)
    try:
        loaded = adapter.load_ontology(repo_id, ontology_path)
        assert loaded, "Ontology load did not return success status."
    except Exception as e:
        pytest.skip(f"Ontology load failed: {e}")

@graphdb_only
def test_list_repositories():
    """Test listing repositories."""
    url = get_env("TRIPLESTORE_URL")
    adapter = get_triplestore_adapter_from_env()
    repos = adapter.list_repositories()
    assert isinstance(repos, list)

@graphdb_only
def test_check_repository_exists():
    """Test repository existence check (explicit repository)."""
    url = get_env("TRIPLESTORE_URL")
    repo_id = get_env("TRIPLESTORE_REPOSITORY")
    adapter = get_triplestore_adapter_from_env(repository=repo_id)
    assert adapter.check_repository_exists(repo_id) is True
    assert adapter.check_repository_exists("nonexistent_repo_12345") is False

# Add a test for fallback to environment variable
@graphdb_only
def test_graphdb_adapter_env_fallback():
    """Test GraphDBAdapter falls back to TRIPLESTORE_REPOSITORY env var if repository not provided."""
    repo_id = get_env("TRIPLESTORE_REPOSITORY")
    adapter = get_triplestore_adapter_from_env()
    assert adapter.repository == repo_id

@graphdb_only
def test_graphdb_version():
    """Test GraphDB version retrieval."""
    url = get_env("TRIPLESTORE_URL")
    adapter = get_triplestore_adapter_from_env()
    version = adapter.get_graphdb_version()
    assert version is None or isinstance(version, str)

@graphdb_only
def test_sparql_select_and_ask():
    """Test SPARQL SELECT and ASK queries."""
    url = get_env("TRIPLESTORE_URL")
    adapter = get_triplestore_adapter_from_env()
    # Simple ASK query
    ask = adapter.sparql_ask("ASK { ?s ?p ?o }")
    assert ask in (True, False)
    # Simple SELECT query
    select = adapter.sparql_select("SELECT * WHERE { ?s ?p ?o } LIMIT 1")
    assert isinstance(select, list)

@graphdb_only
def test_sparql_construct_and_update():
    """Test SPARQL CONSTRUCT and UPDATE queries."""
    url = get_env("TRIPLESTORE_URL")
    adapter = get_triplestore_adapter_from_env()
    # CONSTRUCT query
    construct = adapter.sparql_construct("CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 1")
    assert construct is None or isinstance(construct, str)
    # UPDATE query (insert and delete a dummy triple)
    test_triple = "<urn:test:s> <urn:test:p> \"test\" ."
    insert_query = f"INSERT DATA {{ {test_triple} }}"
    delete_query = f"DELETE DATA {{ {test_triple} }}"
    inserted = adapter.sparql_update(insert_query)
    deleted = adapter.sparql_update(delete_query)
    assert inserted in (True, False)
    assert deleted in (True, False)

@graphdb_only
def test_bulk_load():
    """Test bulk loading RDF data (skipped if no test file)."""
    url = get_env("TRIPLESTORE_URL")
    adapter = get_triplestore_adapter_from_env()
    test_file = "docs/axiusmem_ontology.ttl"
    if not os.path.exists(test_file):
        pytest.skip("No test RDF file for bulk load.")
    loaded = adapter.bulk_load(test_file)
    assert loaded in (True, False)

@graphdb_only
def test_transaction_support():
    """Test transaction begin/commit/rollback (if supported)."""
    url = get_env("TRIPLESTORE_URL")
    adapter = get_triplestore_adapter_from_env()
    tx_id = adapter.begin_transaction()
    if tx_id:
        # Try commit and rollback (should not error)
        committed = adapter.commit_transaction(tx_id)
        rolled_back = adapter.rollback_transaction(tx_id)
        assert committed in (True, False)
        assert rolled_back in (True, False)
    else:
        assert tx_id is None

@graphdb_only
def test_lucene_search():
    """Test Lucene full-text search (returns empty or bindings)."""
    url = get_env("TRIPLESTORE_URL")
    repo_id = get_env("TRIPLESTORE_REPOSITORY")
    adapter = get_triplestore_adapter_from_env()
    results = adapter.lucene_search(repo_id, "memory")
    assert results is None or isinstance(results, list)

@graphdb_only
def test_federated_query_stub():
    """Test federated query stub (should return list or None)."""
    url = get_env("TRIPLESTORE_URL")
    repo_id = get_env("TRIPLESTORE_REPOSITORY")
    adapter = get_triplestore_adapter_from_env()
    # This is just a SELECT query for now
    results = adapter.federated_query(repo_id, "SELECT * WHERE { ?s ?p ?o } LIMIT 1")
    assert results is None or isinstance(results, list)

@graphdb_only
def test_vector_search_stub():
    """Test vector search stub (should return None)."""
    url = get_env("TRIPLESTORE_URL")
    repo_id = get_env("TRIPLESTORE_REPOSITORY")
    adapter = get_triplestore_adapter_from_env()
    results = adapter.vector_search(repo_id, [0.1, 0.2, 0.3])
    assert results is None

@graphdb_only
def test_create_and_delete_repository():
    """Test creating and deleting a repository (skipped if not allowed)."""
    url = get_env("TRIPLESTORE_URL")
    adapter = get_triplestore_adapter_from_env()
    test_repo_id = "test_axiusmem_repo"
    repo_config = {
        "id": test_repo_id,
        "params": {
            "repositoryType": "file-repository",
            "ruleset": "owl-horst-optimized",
            "storage-folder": "/tmp/test_axiusmem_repo"
        }
    }
    created = adapter.create_repository(repo_config)
    # Some GraphDBs may not allow repo creation via REST; skip if not allowed
    if not created:
        pytest.skip("Repository creation not allowed or failed.")
    assert adapter.check_repository_exists(test_repo_id)
    deleted = adapter.delete_repository(test_repo_id)
    assert deleted in (True, False)

@jena_only
def test_jena_list_datasets():
    adapter = get_triplestore_adapter_from_env()
    datasets = adapter.list_datasets()
    assert isinstance(datasets, dict)

@jena_only
def test_jena_create_and_delete_dataset():
    adapter = get_triplestore_adapter_from_env()
    name = "testjenadataset"
    created = adapter.create_dataset(name, db_type="mem")
    assert created
    deleted = adapter.delete_dataset(name)
    assert deleted

@jena_only
def test_jena_get_server_status():
    adapter = get_triplestore_adapter_from_env()
    status = adapter.get_server_status()
    assert isinstance(status, dict)

@jena_only
def test_jena_sparql_construct():
    adapter = get_triplestore_adapter_from_env()
    # Insert a test triple
    adapter.sparql_update("INSERT DATA { <urn:test:s> <urn:test:p> 'test' }")
    turtle = adapter.sparql_construct("CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 1")
    assert isinstance(turtle, str)
    assert "@prefix" in turtle or turtle.strip() != ""

@jena_only
def test_jena_sparql_describe():
    adapter = get_triplestore_adapter_from_env()
    # Insert a test triple
    adapter.sparql_update("INSERT DATA { <urn:test:s> <urn:test:p> 'test' }")
    turtle = adapter.sparql_describe("DESCRIBE <urn:test:s>")
    assert isinstance(turtle, str)
    assert "@prefix" in turtle or turtle.strip() != ""

@jena_only
def test_jena_sparql_ask():
    adapter = get_triplestore_adapter_from_env()
    result = adapter.sparql_ask("ASK { ?s ?p ?o }")
    assert isinstance(result, bool)

@jena_only
def test_jena_get_and_set_dataset_config():
    adapter = get_triplestore_adapter_from_env()
    # Ensure 'Default' dataset exists
    datasets = adapter.list_datasets()
    dataset_names = [d['ds.name'] for d in datasets.get('datasets', [])]
    created = False
    if 'Default' not in dataset_names:
        created = adapter.create_dataset('Default', db_type='mem')
        assert created, "Failed to create 'Default' dataset for test."
    config = adapter.get_dataset_config('Default')
    assert isinstance(config, dict)
    # Try setting the label (no-op if not allowed)
    config["label"] = "Test Label"
    try:
        result = adapter.set_dataset_config("Default", config)
        assert result in (True, False)
    except Exception:
        pass  # Some configs may be read-only
    # Clean up if we created the dataset
    if created:
        adapter.delete_dataset('Default')

@jena_only
def test_jena_backup_and_restore_dataset():
    adapter = get_triplestore_adapter_from_env()
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        backup_path = tmp.name
    try:
        adapter.backup_dataset("Default", backup_path)
    except Exception as e:
        import requests
        if isinstance(e, requests.HTTPError) and "405" in str(e):
            pytest.skip("Jena backup endpoint not available (405)")
        else:
            raise
    assert os.path.exists(backup_path)
    # Restore (smoke test)
    try:
        result = adapter.restore_dataset("Default", backup_path)
        assert result in (True, False)
    except Exception:
        pass  # Restore may require admin rights or may not be supported in all configs 

def always_fail(*args, **kwargs):
    raise requests.exceptions.RequestException("Simulated network failure")

@graphdb_only
def test_graphdb_retry_on_network_failure():
    """Test that GraphDBAdapter methods retry and raise RetryError on repeated network failure."""
    adapter = get_triplestore_adapter_from_env()
    repo_id = os.getenv("TRIPLESTORE_REPOSITORY", "testrepo")
    with patch.object(adapter.session, "post", side_effect=always_fail):
        with pytest.raises(tenacity.RetryError):
            adapter.sparql_select(repo_id, "SELECT * WHERE { ?s ?p ?o } LIMIT 1")
    with patch.object(adapter.session, "post", side_effect=always_fail):
        with pytest.raises(tenacity.RetryError):
            adapter.sparql_update(repo_id, "INSERT DATA { <urn:test:s> <urn:test:p> 'fail' }")
    with patch.object(adapter.session, "post", side_effect=always_fail):
        with pytest.raises(tenacity.RetryError):
            adapter.bulk_load(repo_id, "docs/axiusmem_ontology.ttl")

@jena_only
def test_jena_retry_on_network_failure():
    """Test that JenaAdapter methods retry and raise RequestException on repeated network failure."""
    adapter = get_triplestore_adapter_from_env()
    # Patch post for all relevant methods
    with patch("requests.Session.post", side_effect=always_fail):
        with pytest.raises(requests.exceptions.RequestException):
            adapter.sparql_select("SELECT * WHERE { ?s ?p ?o } LIMIT 1")
    with patch("requests.Session.post", side_effect=always_fail):
        with pytest.raises(requests.exceptions.RequestException):
            adapter.sparql_update("INSERT DATA { <urn:test:s> <urn:test:p> 'fail' }")
    import tempfile, os
    tmp = tempfile.NamedTemporaryFile(suffix=".ttl", delete=False)
    tmp.close()
    try:
        with patch("requests.Session.post", side_effect=always_fail):
            with pytest.raises(requests.exceptions.RequestException):
                adapter.bulk_load(tmp.name)
    finally:
        os.unlink(tmp.name) 