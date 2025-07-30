from .base import BaseTriplestoreAdapter

class StardogAdapter(BaseTriplestoreAdapter):
    """
    Adapter for Stardog (stub).
    See: https://docs.stardog.com/
    """
    def connect(self):
        """Establish a connection to Stardog (not implemented)."""
        raise NotImplementedError("StardogAdapter.connect() not implemented.")

    def close(self):
        """Close the connection to Stardog (not implemented)."""
        raise NotImplementedError("StardogAdapter.close() not implemented.")

    def sparql_select(self, query: str, **kwargs):
        """Execute a SPARQL SELECT query on Stardog (not implemented)."""
        raise NotImplementedError("StardogAdapter.sparql_select() not implemented.")

    def sparql_update(self, update_query: str, **kwargs):
        """Execute a SPARQL UPDATE query on Stardog (not implemented)."""
        raise NotImplementedError("StardogAdapter.sparql_update() not implemented.")

    def bulk_load(self, rdf_path: str, rdf_format: str = "text/turtle"):
        """Bulk load RDF data into Stardog (not implemented)."""
        raise NotImplementedError("StardogAdapter.bulk_load() not implemented.")

    def test_connection(self):
        """Test the connection to Stardog (not implemented)."""
        raise NotImplementedError("StardogAdapter.test_connection() not implemented.") 