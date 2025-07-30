from .base import BaseTriplestoreAdapter

class FourStoreAdapter(BaseTriplestoreAdapter):
    """
    Adapter for 4store (stub).
    See: https://4store.org/
    """
    def connect(self):
        """Establish a connection to 4store (not implemented)."""
        raise NotImplementedError("FourStoreAdapter.connect() not implemented.")

    def close(self):
        """Close the connection to 4store (not implemented)."""
        raise NotImplementedError("FourStoreAdapter.close() not implemented.")

    def sparql_select(self, query: str, **kwargs):
        """Execute a SPARQL SELECT query on 4store (not implemented)."""
        raise NotImplementedError("FourStoreAdapter.sparql_select() not implemented.")

    def sparql_update(self, update_query: str, **kwargs):
        """Execute a SPARQL UPDATE query on 4store (not implemented)."""
        raise NotImplementedError("FourStoreAdapter.sparql_update() not implemented.")

    def bulk_load(self, rdf_path: str, rdf_format: str = "text/turtle"):
        """Bulk load RDF data into 4store (not implemented)."""
        raise NotImplementedError("FourStoreAdapter.bulk_load() not implemented.")

    def test_connection(self):
        """Test the connection to 4store (not implemented)."""
        raise NotImplementedError("FourStoreAdapter.test_connection() not implemented.") 