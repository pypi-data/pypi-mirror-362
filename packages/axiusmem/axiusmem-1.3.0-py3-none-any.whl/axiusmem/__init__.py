"""
AxiusMEM™: A W3C-compliant temporal knowledge graph library for AI agents.
Supports RDF, SPARQL, OWL, bi-temporal data, and GraphDB integration.
"""
from .core import AxiusMEM
from .graphdb_adapter import GraphDBAdapter
from .temporal import *
from .agent_utils import *
from .orm import *
from .query_engine import *
from .utils import *

import importlib.resources
import tempfile
import shutil

__version__ = "1.3.0"

def get_default_ontology_path():
    """
    Returns a file path to the distributed axiusmem_ontology.ttl, regardless of install mode.
    """
    try:
        with importlib.resources.path("axiusmem", "axiusmem_ontology.ttl") as p:
            return str(p)
    except Exception:
        # Fallback: open as file-like and write to temp file
        with importlib.resources.open_text("axiusmem", "axiusmem_ontology.ttl") as f, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".ttl") as tmp:
            shutil.copyfileobj(f, tmp)
            return tmp.name

def load_default_ontology(adapter):
    """
    Loads the distributed axiusmem_ontology.ttl into the given triplestore adapter.
    Usage: after loading environment variables and creating the adapter, call this function.
    """
    ontology_path = get_default_ontology_path()
    adapter.bulk_load(ontology_path)
    return ontology_path 