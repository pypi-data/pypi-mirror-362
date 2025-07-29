from .base import BaseTriplestoreAdapter

class AllegroGraphAdapter(BaseTriplestoreAdapter):
    """
    Adapter for AllegroGraph (Franz Inc.) (stub).
    See: https://franz.com/agraph/support/documentation/current/
    """
    def connect(self):
        """Establish a connection to AllegroGraph (not implemented)."""
        raise NotImplementedError("AllegroGraphAdapter.connect() not implemented.")

    def close(self):
        """Close the connection to AllegroGraph (not implemented)."""
        raise NotImplementedError("AllegroGraphAdapter.close() not implemented.")

    def sparql_select(self, query: str, **kwargs):
        """Execute a SPARQL SELECT query on AllegroGraph (not implemented)."""
        raise NotImplementedError("AllegroGraphAdapter.sparql_select() not implemented.")

    def sparql_update(self, update_query: str, **kwargs):
        """Execute a SPARQL UPDATE query on AllegroGraph (not implemented)."""
        raise NotImplementedError("AllegroGraphAdapter.sparql_update() not implemented.")

    def bulk_load(self, rdf_path: str, rdf_format: str = "text/turtle"):
        """Bulk load RDF data into AllegroGraph (not implemented)."""
        raise NotImplementedError("AllegroGraphAdapter.bulk_load() not implemented.")

    def test_connection(self):
        """Test the connection to AllegroGraph (not implemented)."""
        raise NotImplementedError("AllegroGraphAdapter.test_connection() not implemented.") 