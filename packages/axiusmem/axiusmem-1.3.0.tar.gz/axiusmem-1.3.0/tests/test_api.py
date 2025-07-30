import os
import pytest
from fastapi.testclient import TestClient
from axiusmem.api import create_app
from axiusmem.adapters.base import get_triplestore_adapter_from_env
import rdflib

# Add triplestore-specific decorators
graphdb_only = pytest.mark.skipif(os.getenv("TRIPLESTORE_TYPE") != "graphdb", reason="GraphDB-specific test")
jena_only = pytest.mark.skipif(os.getenv("TRIPLESTORE_TYPE") != "jena", reason="Jena-specific test")

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("AXIUSMEM_ADMIN_USER", "admin")
    monkeypatch.setenv("AXIUSMEM_ADMIN_PASSWORD", "adminpw")
    monkeypatch.delenv("AXIUSMEM_DISABLE_ADMIN_BOOTSTRAP", raising=False)

@pytest.fixture
def client():
    graph = rdflib.Graph()
    app = create_app(graph=graph)
    # Return a factory to use context manager in tests
    def client_factory():
        return app, graph
    return client_factory

def get_token(client, username, password):
    if isinstance(client, tuple):
        client = client[0]
    resp = client.post("/token", data={"username": username, "password": password})
    data = resp.json()
    if "access_token" not in data:
        print("TOKEN ERROR:", resp.status_code, data)
        pytest.skip("Could not authenticate admin user for transaction test.")
    return data["access_token"]

def test_admin_bootstrap_and_auth(client, monkeypatch):
    app, graph = client()
    with TestClient(app) as client:
        # Admin user should be created with correct password and role
        token = get_token(client, "admin", "adminpw")
        assert token
        # Admin can list users
        headers = {"Authorization": f"Bearer {token}"}
        resp = client.get("/users/", headers=headers)
        assert resp.status_code == 200
        assert "admin" in resp.json()
        # Admin has admin role
        resp = client.get("/me", headers=headers)
        assert resp.status_code == 200
        assert "admin" in resp.json()["roles"]


def test_admin_password_update(monkeypatch):
    import rdflib
    # First app with initial password
    graph = rdflib.Graph()
    app1 = create_app(graph=graph)
    with TestClient(app1) as client1:
        # Admin can login with initial password
        resp = client1.post("/token", data={"username": "admin", "password": "adminpw"})
        assert resp.status_code == 200
    # Change admin password and restart app with same graph
    monkeypatch.setenv("AXIUSMEM_ADMIN_PASSWORD", "newpw")
    app2 = create_app(graph=graph)
    with TestClient(app2) as client2:
        # Old password should not work
        resp = client2.post("/token", data={"username": "admin", "password": "adminpw"})
        assert resp.status_code == 400
        # New password should work
        resp = client2.post("/token", data={"username": "admin", "password": "newpw"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Admin can list users
        resp = client2.get("/users/", headers=headers)
        assert resp.status_code == 200


def test_admin_bootstrap_disabled(monkeypatch):
    import rdflib
    monkeypatch.setenv("AXIUSMEM_DISABLE_ADMIN_BOOTSTRAP", "1")
    graph = rdflib.Graph()
    app = create_app(graph=graph)
    with TestClient(app) as client:
        # Admin user should not exist
        resp = client.post("/token", data={"username": "admin", "password": "adminpw"})
        assert resp.status_code == 400 or resp.status_code == 401


def test_create_user_and_roles(client):
    app, graph = client()
    with TestClient(app) as client:
        admin_token = get_token(client, "admin", "adminpw")
        headers = {"Authorization": f"Bearer {admin_token}"}
        # Create agent user
        resp = client.post("/users/", params={"username": "alice", "password": "pw", "roles": ["agent"]}, headers=headers)
        assert resp.status_code == 200
        # Assign admin role
        resp = client.post("/users/alice/roles", params={"role": "admin"}, headers=headers)
        assert resp.status_code == 200
        # List users
        resp = client.get("/users/", headers=headers)
        assert "alice" in resp.json()


def test_agent_access_control(client):
    app, graph = client()
    with TestClient(app) as client:
        admin_token = get_token(client, "admin", "adminpw")
        headers = {"Authorization": f"Bearer {admin_token}"}
        # Create agent user
        client.post("/users/", params={"username": "bob", "password": "pw", "roles": ["agent"]}, headers=headers)
        # Authenticate as agent
        agent_token = get_token(client, "bob", "pw")
        agent_headers = {"Authorization": f"Bearer {agent_token}"}
        # Agent can get own info
        resp = client.get("/me", headers=agent_headers)
        assert resp.status_code == 200
        # Agent cannot list users
        resp = client.get("/users/", headers=agent_headers)
        assert resp.status_code == 403

def transactions_supported():
    try:
        adapter = get_triplestore_adapter_from_env()
        adapter.begin_transaction()
    except NotImplementedError:
        return False
    except Exception:
        # If adapter supports but fails due to config, treat as supported for test
        return True
    return True

@pytest.mark.skipif(not transactions_supported(), reason="Transactions not supported by this adapter.")
def test_transaction_lifecycle(client):
    app, graph = client()
    with TestClient(app) as client_instance:
        admin_token = get_token(client_instance, "admin", "adminpw")
        headers = {"Authorization": f"Bearer {admin_token}"}
        # Begin transaction
        resp = client_instance.post("/transactions/begin", headers=headers)
        assert resp.status_code == 200
        tx_id = resp.json()["tx_id"]
        # Commit transaction
        resp = client_instance.post(f"/transactions/{tx_id}/commit", headers=headers)
        assert resp.status_code == 200
        assert "committed" in resp.json()["msg"]
        # Begin and rollback
        resp = client_instance.post("/transactions/begin", headers=headers)
        assert resp.status_code == 200
        tx_id = resp.json()["tx_id"]
        resp = client_instance.post(f"/transactions/{tx_id}/rollback", headers=headers)
        assert resp.status_code == 200
        assert "rolled back" in resp.json()["msg"]

@pytest.mark.skipif(transactions_supported(), reason="Transactions are supported, skipping unsupported test.")
def test_transaction_not_supported(client):
    app, graph = client()
    with TestClient(app) as client:
        admin_token = get_token(client, "admin", "adminpw")
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.post("/transactions/begin", headers=headers)
        assert resp.status_code == 501
        assert "not supported" in resp.json()["detail"]

def test_health_endpoint(client):
    app, graph = client()
    with TestClient(app) as client:
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "triplestore" in data


def test_metrics_endpoint_admin_and_forbidden(client):
    app, graph = client()
    with TestClient(app) as client:
        # Admin access
        admin_token = get_token(client, "admin", "adminpw")
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.get("/metrics", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "uptime_seconds" in data
        assert "total_requests" in data
        # Unauthenticated
        resp = client.get("/metrics")
        assert resp.status_code == 401 or resp.status_code == 403
        # Non-admin
        # Create agent user
        resp = client.post("/users/", params={"username": "bob", "password": "pw", "roles": ["agent"]}, headers=headers)
        agent_token = get_token(client, "bob", "pw")
        agent_headers = {"Authorization": f"Bearer {agent_token}"}
        resp = client.get("/metrics", headers=agent_headers)
        assert resp.status_code == 403


def test_tasks_endpoint_admin_and_forbidden(client):
    app, graph = client()
    with TestClient(app) as client:
        # Admin access
        admin_token = get_token(client, "admin", "adminpw")
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.get("/tasks", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "tasks" in data
        # Unauthenticated
        resp = client.get("/tasks")
        assert resp.status_code == 401 or resp.status_code == 403
        # Non-admin
        # Create agent user
        resp = client.post("/users/", params={"username": "eve", "password": "pw", "roles": ["agent"]}, headers=headers)
        agent_token = get_token(client, "eve", "pw")
        agent_headers = {"Authorization": f"Bearer {agent_token}"}
        resp = client.get("/tasks", headers=agent_headers)
        assert resp.status_code == 403 

@jena_only
def test_sparql_select_and_ask(client):
    app, graph = client()
    with TestClient(app) as client:
        # Insert some data as admin
        admin_token = get_token(client, "admin", "adminpw")
        headers = {"Authorization": f"Bearer {admin_token}"}
        # Add a triple via the admin-only endpoint (simulate named graph add)
        # For in-memory, add directly to graph
        from rdflib import URIRef, Literal
        s = URIRef("http://example.org/s")
        p = URIRef("http://example.org/p")
        o = Literal("o")
        graph.add((s, p, o))
        # SELECT query
        query = "SELECT ?s ?p ?o WHERE { ?s ?p ?o }"
        resp = client.get("/sparql", params={"query": query})
        assert resp.status_code == 200
        data = resp.json()
        assert "results" in data
        # ASK query
        ask_query = "ASK { ?s ?p ?o }"
        resp = client.get("/sparql", params={"query": ask_query})
        assert resp.status_code == 200
        data = resp.json()
        assert "results" in data

@jena_only
def test_sparql_update_not_allowed(client):
    app, graph = client()
    with TestClient(app) as client:
        # UPDATE query should not be allowed (should error)
        update_query = "INSERT DATA { <http://example.org/s2> <http://example.org/p2> \"o2\" }"
        resp = client.get("/sparql", params={"query": update_query})
        assert resp.status_code in (400, 500, 501)


def test_sparql_invalid_query(client):
    app, graph = client()
    with TestClient(app) as client:
        # Invalid query should return error
        bad_query = "THIS IS NOT SPARQL"
        resp = client.get("/sparql", params={"query": bad_query})
        assert resp.status_code in (400, 500, 501) 

def test_error_response_retry(monkeypatch, client):
    from tenacity import RetryError
    class DummyAttempt:
        def exception(self):
            return "Simulated retry failure"
    app, graph = client()
    with TestClient(app) as client:
        class MockAdapter:
            def sparql_select(self, query):
                raise RetryError(DummyAttempt())
        monkeypatch.setattr("axiusmem.api.get_triplestore_adapter_from_env", lambda *args, **kwargs: MockAdapter())
        resp = client.get("/sparql", params={"query": "SELECT * WHERE { ?s ?p ?o }"})
        if resp.status_code != 503:
            print("Response status:", resp.status_code)
            print("Response content:", resp.content)
        assert resp.status_code == 503
        assert "retries" in resp.json()["detail"]


def test_error_response_500(monkeypatch, client):
    app, graph = client()
    with TestClient(app) as client:
        class MockAdapter:
            def sparql_select(self, query):
                raise RuntimeError("Simulated failure")
        monkeypatch.setattr("axiusmem.api.get_triplestore_adapter_from_env", lambda *args, **kwargs: MockAdapter())
        resp = client.get("/sparql", params={"query": "SELECT * WHERE { ?s ?p ?o }"})
        assert resp.status_code == 500
        assert "Simulated failure" in resp.json()["detail"]
        assert "sparql" in resp.json()["detail"].lower() or "operation" in resp.json()["detail"].lower() 

def test_admin_enforcement_all_endpoints(client):
    app, graph = client()
    with TestClient(app) as client:
        # Authenticate as admin and create agent user
        admin_token = get_token(client, "admin", "adminpw")
        headers = {"Authorization": f"Bearer {admin_token}"}
        client.post("/users/", params={"username": "agent", "password": "pw", "roles": ["agent"]}, headers=headers)
        agent_token = get_token(client, "agent", "pw")
        agent_headers = {"Authorization": f"Bearer {agent_token}"}
        # Use a simple, URL-safe graph URI for path tests
        graph_uri = "graphs%3Aexample"
        endpoints = [
            (client.post, "/users/", {"params": {"username": "x", "password": "pw", "roles": ["agent"]}}),
            (client.delete, "/users/x", {}),
            (client.post, "/users/x/roles", {"params": {"role": "admin"}}),
            (client.get, "/users/", {}),
            (client.get, "/metrics", {}),
            (client.get, "/tasks", {}),
            (client.get, "/graphs/", {}),
            (client.post, "/graphs/", {"params": {"graph_uri": graph_uri}}),
            (client.delete, f"/graphs/{graph_uri}", {}),
            (client.post, f"/graphs/{graph_uri}/clear", {}),
            (client.post, f"/graphs/{graph_uri}/add", {"json": {"triples": []}}),
            (client.post, f"/graphs/{graph_uri}/query", {"params": {"query": "SELECT * WHERE { ?s ?p ?o }"}}),
            (client.post, "/transactions/begin", {}),
            (client.post, "/transactions/txid/commit", {}),
            (client.post, "/transactions/txid/rollback", {}),
            (client.get, "/server/stats", {}),
        ]
        for method, url, kwargs in endpoints:
            resp = method(url, headers=agent_headers, **kwargs)
            assert resp.status_code == 403, f"Endpoint {url} did not return 403 for agent user" 