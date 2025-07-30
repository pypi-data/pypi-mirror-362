from .base import BaseTriplestoreAdapter

class JenaSDBAdapter(BaseTriplestoreAdapter):
    """
    Adapter for Jena SDB (stub).
    See: https://jena.apache.org/documentation/sdb/
    """
    def connect(self):
        """Establish a connection to Jena SDB (not implemented)."""
        raise NotImplementedError("JenaSDBAdapter.connect() not implemented.")

    def close(self):
        """Close the connection to Jena SDB (not implemented)."""
        raise NotImplementedError("JenaSDBAdapter.close() not implemented.")

    def sparql_select(self, query: str, **kwargs):
        """Execute a SPARQL SELECT query on Jena SDB (not implemented)."""
        raise NotImplementedError("JenaSDBAdapter.sparql_select() not implemented.")

    def sparql_update(self, update_query: str, **kwargs):
        """Execute a SPARQL UPDATE query on Jena SDB (not implemented)."""
        raise NotImplementedError("JenaSDBAdapter.sparql_update() not implemented.")

    def bulk_load(self, rdf_path: str, rdf_format: str = "text/turtle"):
        """Bulk load RDF data into Jena SDB (not implemented)."""
        raise NotImplementedError("JenaSDBAdapter.bulk_load() not implemented.")

    def test_connection(self):
        """Test the connection to Jena SDB (not implemented)."""
        raise NotImplementedError("JenaSDBAdapter.test_connection() not implemented.") 