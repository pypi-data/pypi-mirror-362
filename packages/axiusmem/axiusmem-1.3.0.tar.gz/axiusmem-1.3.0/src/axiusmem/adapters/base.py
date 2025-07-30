import abc

class BaseTriplestoreAdapter(abc.ABC):
    """
    Abstract base class for all triplestore adapters in AxiusMEM™.
    Defines the required interface for RDF store integration, including transaction support.
    """
    @abc.abstractmethod
    def connect(self):
        """Establish a connection to the triplestore."""
        pass

    @abc.abstractmethod
    def close(self):
        """Close the connection to the triplestore."""
        pass

    @abc.abstractmethod
    def sparql_select(self, query: str, **kwargs):
        """Execute a SPARQL SELECT query."""
        pass

    @abc.abstractmethod
    def sparql_update(self, update_query: str, **kwargs):
        """Execute a SPARQL UPDATE query."""
        pass

    @abc.abstractmethod
    def bulk_load(self, rdf_path: str, rdf_format: str = "text/turtle"):
        """Bulk load RDF data into the triplestore."""
        pass

    @abc.abstractmethod
    def test_connection(self):
        """Test the connection to the triplestore."""
        pass

    # Transaction support
    @abc.abstractmethod
    def begin_transaction(self):
        """Begin a new transaction. Returns a transaction ID or handle."""
        pass

    @abc.abstractmethod
    def commit_transaction(self, tx_id):
        """Commit the transaction with the given ID."""
        pass

    @abc.abstractmethod
    def rollback_transaction(self, tx_id):
        """Rollback the transaction with the given ID."""
        pass

    # Named graph management
    @abc.abstractmethod
    def list_named_graphs(self):
        """List all named graphs in the triplestore."""
        pass

    @abc.abstractmethod
    def create_named_graph(self, graph_uri):
        """Create a new named graph (may be a no-op for some stores)."""
        pass

    @abc.abstractmethod
    def delete_named_graph(self, graph_uri):
        """Delete a named graph and all its triples."""
        pass

    @abc.abstractmethod
    def clear_named_graph(self, graph_uri):
        """Remove all triples from a named graph, but keep the graph itself."""
        pass

    @abc.abstractmethod
    def add_triples_to_named_graph(self, graph_uri, triples):
        """Add triples to a named graph."""
        pass

    @abc.abstractmethod
    def get_triples_from_named_graph(self, graph_uri, query):
        """Run a SPARQL query against a named graph and return results."""
        pass


def get_triplestore_adapter_from_env(repository=None):
    """
    Factory to instantiate the correct triplestore adapter based on environment variables or explicit repository/dataset.

    Args:
        repository (str, optional): Repository or dataset name. If not provided, falls back to TRIPLESTORE_REPOSITORY env var.

    Reads:
        TRIPLESTORE_TYPE: 'graphdb', 'jena', etc.
        TRIPLESTORE_URL: base URL or host
        TRIPLESTORE_USER: username (optional)
        TRIPLESTORE_PASSWORD: password (optional)
        TRIPLESTORE_REPOSITORY: repository or dataset name (optional, used as fallback)

    Returns:
        An instance of the appropriate triplestore adapter.

    Raises:
        ValueError: If TRIPLESTORE_TYPE is unknown or required variables are missing.
    """
    import os
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # dotenv is optional, skip if not available
    ttype = os.getenv("TRIPLESTORE_TYPE")
    url = os.getenv("TRIPLESTORE_URL")
    user = os.getenv("TRIPLESTORE_USER")
    password = os.getenv("TRIPLESTORE_PASSWORD")
    repo = repository or os.getenv("TRIPLESTORE_REPOSITORY")
    # Import adapters here to avoid circular imports
    from axiusmem.graphdb_adapter import GraphDBAdapter
    from axiusmem.adapters.jena_adapter import JenaAdapter
    # Add more imports as adapters are implemented
    if ttype == "graphdb":
        if not url:
            raise ValueError("TRIPLESTORE_URL must be set for GraphDB.")
        return GraphDBAdapter(url, user, password, repository=repo)
    elif ttype == "jena":
        if not url or not repo:
            raise ValueError("TRIPLESTORE_URL and repository/dataset must be set for Jena.")
        # Parse host/port from url if needed
        import re
        m = re.match(r"https?://([^:/]+)(?::(\d+))?", url)
        host = m.group(1) if m else url
        port = int(m.group(2)) if m and m.group(2) else 3030
        protocol = "https" if url.startswith("https://") else "http"
        return JenaAdapter(host=host, port=port, dataset=repo, username=user, password=password, protocol=protocol)
    else:
        raise ValueError(f"Unknown TRIPLESTORE_TYPE: {ttype}") 