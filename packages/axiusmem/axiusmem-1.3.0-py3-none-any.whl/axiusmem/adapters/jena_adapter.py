import requests
from requests.auth import HTTPBasicAuth
from .base import BaseTriplestoreAdapter
import tenacity

# Retry config: 3 attempts, exponential backoff, retry on network/HTTP 5xx
retry_on_network = tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=0.5, min=1, max=8),
    retry=tenacity.retry_if_exception_type((requests.exceptions.RequestException,)),
    reraise=True,
    before_sleep=tenacity.before_sleep_log(__import__('logging').getLogger("axiusmem.jena_adapter"), __import__('logging').WARNING)
)

# AxiusMEM™ Jena Adapter
class JenaAdapter(BaseTriplestoreAdapter):
    """
    Adapter for Apache Jena (TDB/Fuseki).
    Connects to a Fuseki server via HTTP.

    Args:
        host (str): Hostname for Jena Fuseki.
        port (int): Port for Jena Fuseki.
        dataset (str, optional): Dataset name. If not provided, falls back to TRIPLESTORE_REPOSITORY env var.
        username (str, optional): Username for authentication.
        password (str, optional): Password for authentication.
        protocol (str, optional): 'http' or 'https'.
    """
    def __init__(self, host='localhost', port=3030, dataset=None, username=None, password=None, protocol='http'):
        import os
        self.host = host
        self.port = port
        self.dataset = dataset or os.getenv("TRIPLESTORE_REPOSITORY")
        self.username = username
        self.password = password
        self.protocol = protocol
        self.session = None
        self.base_url = None

    def connect(self):
        """Establish a connection to Jena Fuseki (sets up session and base URL)."""
        self.base_url = f"{self.protocol}://{self.host}:{self.port}/{self.dataset}"
        self.session = requests.Session()
        if self.username and self.password:
            self.session.auth = HTTPBasicAuth(self.username, self.password)

    def close(self):
        """Close the session to Jena Fuseki."""
        if self.session:
            self.session.close()
            self.session = None

    @retry_on_network
    def sparql_select(self, query: str, **kwargs):
        """Execute a SPARQL SELECT query on Jena Fuseki."""
        if not self.session:
            self.connect()
        endpoint = f"{self.base_url}/sparql"
        headers = {'Accept': 'application/sparql-results+json'}
        data = {'query': query}
        response = self.session.post(endpoint, data=data, headers=headers, timeout=kwargs.get('timeout', 30))
        response.raise_for_status()
        return response.json()

    @retry_on_network
    def sparql_update(self, update_query: str, **kwargs):
        """Execute a SPARQL UPDATE query on Jena Fuseki."""
        if not self.session:
            self.connect()
        endpoint = f"{self.base_url}/update"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'update': update_query}
        response = self.session.post(endpoint, data=data, headers=headers, timeout=kwargs.get('timeout', 30))
        response.raise_for_status()
        return response.text

    @retry_on_network
    def bulk_load(self, rdf_path: str, rdf_format: str = "text/turtle"):
        """Bulk load RDF data into Jena Fuseki using the /data endpoint."""
        if not self.session:
            self.connect()
        endpoint = f"{self.base_url}/data"
        headers = {'Content-Type': rdf_format}
        with open(rdf_path, 'rb') as f:
            data = f.read()
        response = self.session.post(endpoint, data=data, headers=headers)
        response.raise_for_status()
        return response.text

    def test_connection(self):
        """Test the connection to Jena Fuseki by running a simple ASK query."""
        try:
            result = self.sparql_select("ASK {}")
            return result.get('boolean', False)
        except Exception as e:
            return False 

    def list_datasets(self):
        """List all datasets (repositories) in the Jena Fuseki server."""
        if not self.session:
            self.connect()
        endpoint = f"{self.protocol}://{self.host}:{self.port}/$/datasets"
        response = self.session.get(endpoint)
        response.raise_for_status()
        return response.json()  # Returns a dict with dataset info

    def create_dataset(self, name: str, db_type: str = "mem"):
        """Create a new dataset in Jena Fuseki. db_type can be 'mem' or 'tdb'."""
        if not self.session:
            self.connect()
        endpoint = f"{self.protocol}://{self.host}:{self.port}/$/datasets"
        data = {"dbType": db_type, "dbName": name}
        response = self.session.post(endpoint, data=data)
        response.raise_for_status()
        return response.status_code == 200 or response.status_code == 201

    def delete_dataset(self, name: str):
        """Delete a dataset from Jena Fuseki."""
        if not self.session:
            self.connect()
        endpoint = f"{self.protocol}://{self.host}:{self.port}/$/datasets/{name}"
        response = self.session.delete(endpoint)
        response.raise_for_status()
        return response.status_code == 200 or response.status_code == 204

    def get_server_status(self):
        """Get the status of the Jena Fuseki server."""
        if not self.session:
            self.connect()
        endpoint = f"{self.protocol}://{self.host}:{self.port}/$/server"
        response = self.session.get(endpoint)
        response.raise_for_status()
        return response.json() 
        
    def sparql_construct(self, query: str, **kwargs):
        """Execute a SPARQL CONSTRUCT query on Jena Fuseki. Returns Turtle RDF as text."""
        if not self.session:
            self.connect()
        endpoint = f"{self.base_url}/sparql"
        headers = {'Accept': 'text/turtle'}
        data = {'query': query}
        response = self.session.post(endpoint, data=data, headers=headers, timeout=kwargs.get('timeout', 30))
        response.raise_for_status()
        return response.text

    def sparql_describe(self, query: str, **kwargs):
        """Execute a SPARQL DESCRIBE query on Jena Fuseki. Returns Turtle RDF as text."""
        if not self.session:
            self.connect()
        endpoint = f"{self.base_url}/sparql"
        headers = {'Accept': 'text/turtle'}
        data = {'query': query}
        response = self.session.post(endpoint, data=data, headers=headers, timeout=kwargs.get('timeout', 30))
        response.raise_for_status()
        return response.text

    def sparql_ask(self, query: str, **kwargs):
        """Execute a SPARQL ASK query on Jena Fuseki. Returns a boolean result."""
        if not self.session:
            self.connect()
        endpoint = f"{self.base_url}/sparql"
        headers = {'Accept': 'application/sparql-results+json'}
        data = {'query': query}
        response = self.session.post(endpoint, data=data, headers=headers, timeout=kwargs.get('timeout', 30))
        response.raise_for_status()
        return response.json().get('boolean', False) 
        
    def get_dataset_config(self, name: str):
        """Get the configuration of a dataset from Jena Fuseki."""
        if not self.session:
            self.connect()
        endpoint = f"{self.protocol}://{self.host}:{self.port}/$/datasets/{name}"
        response = self.session.get(endpoint)
        response.raise_for_status()
        return response.json()

    def set_dataset_config(self, name: str, config: dict):
        """Set the configuration of a dataset in Jena Fuseki. config should be a dict."""
        if not self.session:
            self.connect()
        endpoint = f"{self.protocol}://{self.host}:{self.port}/$/datasets/{name}"
        response = self.session.put(endpoint, json=config)
        response.raise_for_status()
        return response.status_code in (200, 204)

    def backup_dataset(self, name: str, out_path: str):
        """Backup a dataset from Jena Fuseki. Saves the backup file to out_path."""
        if not self.session:
            self.connect()
        endpoint = f"{self.protocol}://{self.host}:{self.port}/$/backup"
        data = {"dbName": name}
        response = self.session.post(endpoint, data=data, stream=True)
        response.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return out_path

    def restore_dataset(self, name: str, backup_path: str):
        """Restore a dataset in Jena Fuseki from a backup file."""
        if not self.session:
            self.connect()
        endpoint = f"{self.protocol}://{self.host}:{self.port}/$/restore"
        files = {"file": open(backup_path, "rb")}
        data = {"dbName": name}
        response = self.session.post(endpoint, data=data, files=files)
        response.raise_for_status()
        return response.status_code in (200, 201, 204) 
        
    def begin_transaction(self):
        """Jena Fuseki does not support HTTP transactions in the standard setup (stub)."""
        raise NotImplementedError("JenaAdapter: Transactions are not supported via HTTP API.")

    def commit_transaction(self, tx_id):
        raise NotImplementedError("JenaAdapter: Transactions are not supported via HTTP API.")

    def rollback_transaction(self, tx_id):
        raise NotImplementedError("JenaAdapter: Transactions are not supported via HTTP API.") 
        
    @retry_on_network
    def list_named_graphs(self):
        query = "SELECT DISTINCT ?g WHERE { GRAPH ?g { ?s ?p ?o } }"
        return self.sparql_select(query)

    @retry_on_network
    def create_named_graph(self, graph_uri):
        # SPARQL 1.1 does not have explicit CREATE GRAPH in Jena, but INSERT DATA can create it
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
            # No-op, but ensures graph exists
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
        # Wrap the query in GRAPH <graph_uri> if not already
        wrapped_query = f"SELECT * WHERE {{ GRAPH <{graph_uri}> {{ {query} }} }}"
        return self.sparql_select(wrapped_query) 
        