"""
AxiusMEM: A W3C-compliant temporal knowledge graph library for AI agents.
Supports RDF, SPARQL, OWL, bi-temporal data, and GraphDB integration.
"""
from .core import AxiusMEM
from .graphdb_adapter import GraphDBAdapter
from .temporal import *
from .agent_utils import *
from .orm import *
from .query_engine import *
from .utils import *

__version__ = "0.1.0a0" 