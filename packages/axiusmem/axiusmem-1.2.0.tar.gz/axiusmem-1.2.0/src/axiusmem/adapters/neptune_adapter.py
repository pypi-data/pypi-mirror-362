from .base import BaseTriplestoreAdapter

class NeptuneAdapter(BaseTriplestoreAdapter):
    """
    Adapter for Amazon Neptune (stub).
    See: https://docs.aws.amazon.com/neptune/latest/userguide/intro.html
    """
    def connect(self):
        """Establish a connection to Neptune (not implemented)."""
        raise NotImplementedError("NeptuneAdapter.connect() not implemented.")

    def close(self):
        """Close the connection to Neptune (not implemented)."""
        raise NotImplementedError("NeptuneAdapter.close() not implemented.")

    def sparql_select(self, query: str, **kwargs):
        """Execute a SPARQL SELECT query on Neptune (not implemented)."""
        raise NotImplementedError("NeptuneAdapter.sparql_select() not implemented.")

    def sparql_update(self, update_query: str, **kwargs):
        """Execute a SPARQL UPDATE query on Neptune (not implemented)."""
        raise NotImplementedError("NeptuneAdapter.sparql_update() not implemented.")

    def bulk_load(self, rdf_path: str, rdf_format: str = "text/turtle"):
        """Bulk load RDF data into Neptune (not implemented)."""
        raise NotImplementedError("NeptuneAdapter.bulk_load() not implemented.")

    def test_connection(self):
        """Test the connection to Neptune (not implemented)."""
        raise NotImplementedError("NeptuneAdapter.test_connection() not implemented.") 