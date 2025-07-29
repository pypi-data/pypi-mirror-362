import rdflib
import os
from dotenv import load_dotenv
from rdflib.namespace import OWL, RDF, RDFS
from typing import List, Tuple, Optional, Union
from .utils import attach_provenance
from .temporal import add_valid_time, add_transaction_time, query_point_in_time, query_as_of
from .query_engine import sparql_select, sparql_construct, sparql_update

class AxiusMEM:
    """
    AxiusMEM: W3C-compliant temporal knowledge graph core for AI agents.

    This class manages an RDF graph, supports ontology loading, bi-temporal data (valid/transaction time),
    provenance, ingestion, querying, and temporal reasoning. It is the main entry point for interacting with
    the AxiusMEM knowledge graph in Python.

    Example:
        >>> mem = AxiusMEM()
        >>> mem.add_triples([(s, p, o)], valid_time={"from": "2024-01-01"})
        >>> results, df = mem.select('SELECT ?s ?o WHERE { ?s <http://example.org/knows> ?o . }')
    """
    def __init__(self, ontology_path: Optional[str] = None, env_path: Optional[str] = None):
        """
        Initialize AxiusMEM and load the ontology.

        Args:
            ontology_path (Optional[str]): Path to the ontology file (Turtle or RDF/XML).
            env_path (Optional[str]): Path to .env file for environment variables.
        """
        load_dotenv(env_path or ".env")
        self.ontology_path = ontology_path or "axiusmem_ontology.ttl"
        self.graph = rdflib.Graph()
        self.ontologies = set()
        self.load_ontology(self.ontology_path)
        self.triplestore_type = os.getenv("TRIPLESTORE_TYPE")
        self.triplestore_url = os.getenv("TRIPLESTORE_URL")
        self.triplestore_user = os.getenv("TRIPLESTORE_USER")
        self.triplestore_password = os.getenv("TRIPLESTORE_PASSWORD")
        self.triplestore_repository = os.getenv("TRIPLESTORE_REPOSITORY")

    def load_ontology(self, ontology_path: str, format: Optional[str] = None) -> None:
        """
        Load an ontology file (Turtle or RDF/XML) into the graph.

        Args:
            ontology_path (str): Path to the ontology file.
            format (Optional[str]): RDF format ("turtle", "xml", etc.).
        """
        fmt = format or ("turtle" if ontology_path.endswith(".ttl") else "xml")
        self.graph.parse(ontology_path, format=fmt)
        self.ontologies.add(ontology_path)

    def extend_ontology(self, triples: List[Tuple[rdflib.term.Identifier, rdflib.term.Identifier, rdflib.term.Identifier]]) -> None:
        """
        Add new triples to the ontology at runtime.

        Args:
            triples (List[Tuple]): List of (subject, predicate, object) triples to add.
        """
        for s, p, o in triples:
            self.graph.add((s, p, o))

    def define_class(self, class_uri: str, label: Optional[str] = None, comment: Optional[str] = None) -> rdflib.URIRef:
        """
        Programmatically define a new RDF class (entity type).

        Args:
            class_uri (str): URI for the new class.
            label (Optional[str]): Human-readable label.
            comment (Optional[str]): Description/comment.

        Returns:
            rdflib.URIRef: The URIRef of the new class.
        """
        class_ref = rdflib.URIRef(class_uri)
        self.graph.add((class_ref, RDF.type, OWL.Class))
        if label:
            self.graph.add((class_ref, RDFS.label, rdflib.Literal(label)))
        if comment:
            self.graph.add((class_ref, RDFS.comment, rdflib.Literal(comment)))
        return class_ref

    def define_property(self, prop_uri: str, domain: Optional[str] = None, range_: Optional[str] = None, label: Optional[str] = None, comment: Optional[str] = None) -> rdflib.URIRef:
        """
        Programmatically define a new RDF property (relationship type).

        Args:
            prop_uri (str): URI for the new property.
            domain (Optional[str]): URI of the domain class.
            range_ (Optional[str]): URI of the range class.
            label (Optional[str]): Human-readable label.
            comment (Optional[str]): Description/comment.

        Returns:
            rdflib.URIRef: The URIRef of the new property.
        """
        prop_ref = rdflib.URIRef(prop_uri)
        self.graph.add((prop_ref, RDF.type, OWL.ObjectProperty))
        if domain:
            self.graph.add((prop_ref, RDFS.domain, rdflib.URIRef(domain)))
        if range_:
            self.graph.add((prop_ref, RDFS.range, rdflib.URIRef(range_)))
        if label:
            self.graph.add((prop_ref, RDFS.label, rdflib.Literal(label)))
        if comment:
            self.graph.add((prop_ref, RDFS.comment, rdflib.Literal(comment)))
        return prop_ref

    def add_triples(
        self,
        triples: List[Tuple[rdflib.term.Identifier, rdflib.term.Identifier, rdflib.term.Identifier]],
        valid_time: Optional[dict] = None,
        transaction_time: Optional[dict] = None,
        provenance: Optional[dict] = None,
    ) -> None:
        """
        Add triples to the graph, optionally with valid/transaction time and provenance.

        Args:
            triples (List[Tuple]): List of (subject, predicate, object) triples to add.
            valid_time (Optional[dict]): Dict with 'from' and optional 'to' (ISO 8601 strings).
            transaction_time (Optional[dict]): Dict with 'from' and optional 'to' (ISO 8601 strings).
            provenance (Optional[dict]): Provenance metadata.

        Example:
            >>> mem.add_triples([(s, p, o)], valid_time={"from": "2024-01-01"})
        """
        for s, p, o in triples:
            self.graph.add((s, p, o))
            if valid_time:
                add_valid_time(self.graph, (s, p, o), valid_time['from'], valid_time.get('to'))
            if transaction_time:
                add_transaction_time(self.graph, (s, p, o), transaction_time['from'], transaction_time.get('to'))
            if provenance:
                attach_provenance((s, p, o), **provenance)

    def update_triple(
        self,
        old_triple: Tuple[rdflib.term.Identifier, rdflib.term.Identifier, rdflib.term.Identifier],
        new_triple: Tuple[rdflib.term.Identifier, rdflib.term.Identifier, rdflib.term.Identifier],
        valid_time: Optional[dict] = None,
        transaction_time: Optional[dict] = None,
        provenance: Optional[dict] = None,
    ) -> None:
        """
        Update a triple: retract old triple, add new triple, preserving temporal/provenance context.

        Args:
            old_triple (Tuple): The triple to retract.
            new_triple (Tuple): The triple to add.
            valid_time (Optional[dict]): Dict with 'from' and optional 'to' (ISO 8601 strings).
            transaction_time (Optional[dict]): Dict with 'from' and optional 'to' (ISO 8601 strings).
            provenance (Optional[dict]): Provenance metadata.
        """
        self.delete_triple(old_triple, transaction_time=transaction_time, provenance=provenance)
        self.add_triples([new_triple], valid_time=valid_time, transaction_time=transaction_time, provenance=provenance)

    def delete_triple(
        self,
        triple: Tuple[rdflib.term.Identifier, rdflib.term.Identifier, rdflib.term.Identifier],
        transaction_time: Optional[dict] = None,
        provenance: Optional[dict] = None,
    ) -> None:
        """
        Delete a triple from the graph, optionally recording transaction time and provenance.

        Args:
            triple (Tuple): The triple to delete.
            transaction_time (Optional[dict]): Dict with 'from' and optional 'to' (ISO 8601 strings).
            provenance (Optional[dict]): Provenance metadata.
        """
        s, p, o = triple
        if (s, p, o) in self.graph:
            self.graph.remove((s, p, o))
            if transaction_time:
                add_transaction_time(self.graph, (s, p, o), transaction_time['from'], transaction_time.get('to'))
            if provenance:
                attach_provenance((s, p, o), **provenance)

    def bulk_load(
        self,
        file_path: str,
        format: str = "turtle",
        valid_time: Optional[dict] = None,
        transaction_time: Optional[dict] = None,
        provenance: Optional[dict] = None,
    ) -> int:
        """
        Batch ingest RDF data from a file. Optionally apply valid/transaction time and provenance to all loaded triples.

        Args:
            file_path (str): Path to the RDF file.
            format (str): RDF format ("turtle", "xml", etc.).
            valid_time (Optional[dict]): Dict with 'from' and optional 'to' (ISO 8601 strings).
            transaction_time (Optional[dict]): Dict with 'from' and optional 'to' (ISO 8601 strings).
            provenance (Optional[dict]): Provenance metadata.

        Returns:
            int: Number of triples added.
        """
        temp_graph = rdflib.Graph()
        temp_graph.parse(file_path, format=format)
        triples = list(temp_graph)
        self.add_triples(triples, valid_time=valid_time, transaction_time=transaction_time, provenance=provenance)
        return len(triples)

    def get_graph(self) -> rdflib.Graph:
        """
        Return the underlying rdflib.Graph object.

        Returns:
            rdflib.Graph: The underlying graph.
        """
        return self.graph

    def validate_triples(self, triples: List[Tuple[rdflib.term.Identifier, rdflib.term.Identifier, rdflib.term.Identifier]]) -> List[str]:
        """
        Validate a list of triples against the loaded ontology.

        Args:
            triples (List[Tuple]): List of (subject, predicate, object) triples to validate.

        Returns:
            List[str]: List of error strings (empty if valid).
        """
        from .utils import validate_data_against_ontology
        return validate_data_against_ontology(self.graph, triples)

    def select(self, query: str):
        """
        Run a SPARQL SELECT query on the knowledge graph.

        Args:
            query (str): The SPARQL SELECT query to run.

        Returns:
            Tuple[List[dict], pandas.DataFrame]: Query results as a list of dicts and a DataFrame.
        """
        return sparql_select(self.graph, query)

    def construct(self, query: str):
        """
        Run a SPARQL CONSTRUCT query on the knowledge graph.

        Args:
            query (str): The SPARQL CONSTRUCT query to run.

        Returns:
            rdflib.Graph: A new graph with the constructed triples.
        """
        return sparql_construct(self.graph, query)

    def update(self, query: str):
        """
        Run a SPARQL UPDATE (INSERT/DELETE) query on the knowledge graph.

        Args:
            query (str): The SPARQL UPDATE query to run.
        """
        return sparql_update(self.graph, query)

    def select_point_in_time(self, query: str, time: str):
        """
        Run a SPARQL SELECT query on the subgraph valid at a specific valid time (ISO 8601 string).

        Args:
            query (str): The SPARQL SELECT query to run.
            time (str): The valid time (ISO 8601 string).

        Returns:
            Tuple[List[dict], pandas.DataFrame]: Query results as a list of dicts and a DataFrame.
        """
        subgraph = query_point_in_time(self.graph, time)
        from .query_engine import sparql_select
        return sparql_select(subgraph, query)

    def select_as_of(self, query: str, transaction_time: str):
        """
        Run a SPARQL SELECT query on the subgraph as known at a specific transaction time (ISO 8601 string).

        Args:
            query (str): The SPARQL SELECT query to run.
            transaction_time (str): The transaction time (ISO 8601 string).

        Returns:
            Tuple[List[dict], pandas.DataFrame]: Query results as a list of dicts and a DataFrame.
        """
        subgraph = query_as_of(self.graph, transaction_time)
        from .query_engine import sparql_select
        return sparql_select(subgraph, query)

    def select_interval_valid_time(self, query: str, start: str, end: str):
        """
        Run a SPARQL SELECT query on the subgraph valid at any point during [start, end] (ISO 8601 strings).

        Args:
            query (str): The SPARQL SELECT query to run.
            start (str): Interval start (ISO 8601 string).
            end (str): Interval end (ISO 8601 string).

        Returns:
            Tuple[List[dict], pandas.DataFrame]: Query results as a list of dicts and a DataFrame.
        """
        from .temporal import query_interval_valid_time
        subgraph = query_interval_valid_time(self.graph, start, end)
        from .query_engine import sparql_select
        return sparql_select(subgraph, query)

    def select_interval_transaction_time(self, query: str, start: str, end: str):
        """
        Run a SPARQL SELECT query on the subgraph known at any point during [start, end] (ISO 8601 strings).

        Args:
            query (str): The SPARQL SELECT query to run.
            start (str): Interval start (ISO 8601 string).
            end (str): Interval end (ISO 8601 string).

        Returns:
            Tuple[List[dict], pandas.DataFrame]: Query results as a list of dicts and a DataFrame.
        """
        from .temporal import query_interval_transaction_time
        subgraph = query_interval_transaction_time(self.graph, start, end)
        from .query_engine import sparql_select
        return sparql_select(subgraph, query)

    def path_query_point_in_time(self, query: str, time: str):
        """
        Run a SPARQL path/traversal query on the subgraph valid at a specific valid time.

        Args:
            query (str): The SPARQL path/traversal query to run.
            time (str): The valid time (ISO 8601 string).

        Returns:
            Tuple[List[dict], pandas.DataFrame]: Query results as a list of dicts and a DataFrame.
        """
        subgraph = query_point_in_time(self.graph, time)
        from .query_engine import sparql_select
        return sparql_select(subgraph, query)

    def path_query_interval_valid_time(self, query: str, start: str, end: str):
        """
        Run a SPARQL path/traversal query on the subgraph valid at any point during [start, end].

        Args:
            query (str): The SPARQL path/traversal query to run.
            start (str): Interval start (ISO 8601 string).
            end (str): Interval end (ISO 8601 string).

        Returns:
            Tuple[List[dict], pandas.DataFrame]: Query results as a list of dicts and a DataFrame.
        """
        from .temporal import query_interval_valid_time
        subgraph = query_interval_valid_time(self.graph, start, end)
        from .query_engine import sparql_select
        return sparql_select(subgraph, query)

    def aggregate_point_in_time(self, query: str, time: str):
        """
        Run a SPARQL aggregation query on the subgraph valid at a specific valid time.

        Args:
            query (str): The SPARQL aggregation query to run.
            time (str): The valid time (ISO 8601 string).

        Returns:
            Tuple[List[dict], pandas.DataFrame]: Query results as a list of dicts and a DataFrame.
        """
        subgraph = query_point_in_time(self.graph, time)
        from .query_engine import sparql_select
        return sparql_select(subgraph, query)

    def aggregate_interval_valid_time(self, query: str, start: str, end: str):
        """
        Run a SPARQL aggregation query on the subgraph valid at any point during [start, end].

        Args:
            query (str): The SPARQL aggregation query to run.
            start (str): Interval start (ISO 8601 string).
            end (str): Interval end (ISO 8601 string).

        Returns:
            Tuple[List[dict], pandas.DataFrame]: Query results as a list of dicts and a DataFrame.
        """
        from .temporal import query_interval_valid_time
        subgraph = query_interval_valid_time(self.graph, start, end)
        from .query_engine import sparql_select
        return sparql_select(subgraph, query)

    # TODO: Add support for inferencing (local and GraphDB-backed)
    # TODO: Add more provenance utilities as needed 