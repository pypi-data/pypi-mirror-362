from .base import BaseTriplestoreAdapter

class DydraAdapter(BaseTriplestoreAdapter):
    """
    Adapter for Dydra (stub).
    See: https://docs.dydra.com/
    """
    def connect(self):
        """Establish a connection to Dydra (not implemented)."""
        raise NotImplementedError("DydraAdapter.connect() not implemented.")

    def close(self):
        """Close the connection to Dydra (not implemented)."""
        raise NotImplementedError("DydraAdapter.close() not implemented.")

    def sparql_select(self, query: str, **kwargs):
        """Execute a SPARQL SELECT query on Dydra (not implemented)."""
        raise NotImplementedError("DydraAdapter.sparql_select() not implemented.")

    def sparql_update(self, update_query: str, **kwargs):
        """Execute a SPARQL UPDATE query on Dydra (not implemented)."""
        raise NotImplementedError("DydraAdapter.sparql_update() not implemented.")

    def bulk_load(self, rdf_path: str, rdf_format: str = "text/turtle"):
        """Bulk load RDF data into Dydra (not implemented)."""
        raise NotImplementedError("DydraAdapter.bulk_load() not implemented.")

    def test_connection(self):
        """Test the connection to Dydra (not implemented)."""
        raise NotImplementedError("DydraAdapter.test_connection() not implemented.") 