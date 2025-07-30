"""
OpenRXN Perovskite Optimizer

AI-driven perovskite solar cell optimization platform with OpenAI Agents SDK.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

__version__ = "1.0.0"
__author__ = "Nik Jois"
__email__ = "nikjois@llamasearch.ai"
__license__ = "MIT"

# Import key components for easy access
from .agents.discovery import MaterialsDiscoveryAgent
from .agents.synthesis import SynthesisAgent
from .agents.optimization import OptimizationAgent
from .models.crystal_structure import PerovskiteStructure
from .models.electronic_properties import ElectronicProperties
from .database.connection import DatabaseManager

__all__ = [
    "MaterialsDiscoveryAgent",
    "SynthesisAgent", 
    "OptimizationAgent",
    "PerovskiteStructure",
    "ElectronicProperties",
    "DatabaseManager",
    "__version__",
    "__author__",
    "__email__"
]
