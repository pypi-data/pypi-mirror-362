import requests
import logging
from typing import Optional, Dict, Any, List, Union
import os
import tenacity
from axiusmem.adapters.base import BaseTriplestoreAdapter

# Retry config: 3 attempts, exponential backoff, retry on network/HTTP 5xx
retry_on_network = tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=0.5, min=1, max=8),
    retry=tenacity.retry_if_exception_type((requests.exceptions.RequestException,)),
    reraise=True,
    before_sleep=tenacity.before_sleep_log(logging.getLogger("axiusmem.graphdb_adapter"), logging.WARNING)
)

# AxiusMEM™ GraphDB Adapter
class GraphDBAdapter(BaseTriplestoreAdapter):
    """
    Adapter for interacting with Ontotext GraphDB via its REST API.
    Inherits from BaseTriplestoreAdapter.

    Args:
        url (str): Base URL for GraphDB.
        user (str, optional): Username for authentication.
        password (str, optional): Password for authentication.
        repository (str, optional): Repository name. If not provided, falls back to TRIPLESTORE_REPOSITORY env var.
        use_https (bool, optional): Use HTTPS for requests (default True).
    """
    def __init__(self, url, user=None, password=None, repository=None, use_https=True):
        import os
        self.url = url.rstrip('/')
        self.user = user
        self.password = password
        self.repository = repository or os.getenv("TRIPLESTORE_REPOSITORY")
        self.use_https = use_https
        self.session = requests.Session()
        if user and password:
            self.session.auth = (user, password)

    def connect(self):
        # No-op for HTTP API, but could test connection
        return self.test_connection()

    def close(self):
        if self.session:
            self.session.close()
            self.session = None

    @retry_on_network
    def sparql_select(self, query: str, **kwargs):
        repo_id = self.repository
        params = {"infer": str(kwargs.get("infer", True)).lower(), "timeout": kwargs.get("timeout", 60)}
        headers = {"Accept": "application/sparql-results+json"}
        resp = self.session.post(
            f"{self.url}/repositories/{repo_id}",
            data={"query": query},
            params=params,
            headers=headers,
            timeout=kwargs.get("timeout", 60)
        )
        resp.raise_for_status()
        return resp.json().get("results", {}).get("bindings", [])

    @retry_on_network
    def sparql_update(self, update_query: str, **kwargs):
        repo_id = self.repository
        headers = {"Content-Type": "application/sparql-update"}
        resp = self.session.post(
            f"{self.url}/repositories/{repo_id}/statements",
            data=update_query.encode("utf-8"),
            headers=headers,
            timeout=kwargs.get("timeout", 60)
        )
        resp.raise_for_status()
        return resp.status_code == 204

    @retry_on_network
    def bulk_load(self, rdf_path: str, rdf_format: str = "text/turtle"):
        repo_id = self.repository
        with open(rdf_path, "rb") as f:
            data = f.read()
        headers = {"Content-Type": rdf_format}
        resp = self.session.post(
            f"{self.url}/repositories/{repo_id}/statements",
            data=data,
            headers=headers
        )
        resp.raise_for_status()
        return resp.status_code == 204

    @retry_on_network
    def test_connection(self):
        try:
            resp = self.session.get(f"{self.url}/rest/repositories")
            resp.raise_for_status()
            return True
        except Exception as e:
            print(f"GraphDB connection failed: {e}")
            return False

    @retry_on_network
    def begin_transaction(self):
        repo_id = self.repository
        resp = self.session.post(f"{self.url}/repositories/{repo_id}/transactions")
        resp.raise_for_status()
        return resp.json()["transactionId"]

    @retry_on_network
    def commit_transaction(self, tx_id):
        repo_id = self.repository
        resp = self.session.put(f"{self.url}/repositories/{repo_id}/transactions/{tx_id}")
        resp.raise_for_status()
        return resp.status_code == 200

    @retry_on_network
    def rollback_transaction(self, tx_id):
        repo_id = self.repository
        resp = self.session.delete(f"{self.url}/repositories/{repo_id}/transactions/{tx_id}")
        resp.raise_for_status()
        return resp.status_code == 200

    @retry_on_network
    def list_named_graphs(self):
        query = "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } }"
        results = self.sparql_select(query)
        return [r['g']['value'] for r in results] if results else []

    @retry_on_network
    def create_named_graph(self, graph_uri):
        return self.add_triples_to_named_graph(graph_uri, [])

    @retry_on_network
    def delete_named_graph(self, graph_uri):
        update = f"DROP GRAPH <{graph_uri}>"
        return self.sparql_update(update)

    @retry_on_network
    def clear_named_graph(self, graph_uri):
        update = f"CLEAR GRAPH <{graph_uri}>"
        return self.sparql_update(update)

    @retry_on_network
    def add_triples_to_named_graph(self, graph_uri, triples):
        if not triples:
            return True
        triple_strs = []
        for s, p, o in triples:
            s_str = f"<{s}>" if not s.startswith("_") else s
            p_str = f"<{p}>"
            o_str = f'"{o}"' if not (str(o).startswith("http://") or str(o).startswith("https://")) else f"<{o}>"
            triple_strs.append(f"{s_str} {p_str} {o_str} .")
        update = f"INSERT DATA {{ GRAPH <{graph_uri}> {{ {' '.join(triple_strs)} }} }}"
        return self.sparql_update(update)

    @retry_on_network
    def get_triples_from_named_graph(self, graph_uri, query):
        wrapped_query = f"SELECT * WHERE {{ GRAPH <{graph_uri}> {{ {query} }} }}"
        return self.sparql_select(wrapped_query) 