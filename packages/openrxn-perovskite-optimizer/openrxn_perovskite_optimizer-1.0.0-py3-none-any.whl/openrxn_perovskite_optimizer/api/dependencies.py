from ..agents.discovery import MaterialsDiscoveryAgent
from ..agents.synthesis import SynthesisAgent
from ..agents.characterization import CharacterizationAgent
from ..agents.optimization import OptimizationAgent
from ..agents.experimental import ExperimentalAgent
from ..database.crud import MaterialsCRUD, ExperimentalCRUD
from ..database.connection import DatabaseManager
from ..ml.property_prediction import PropertyPredictor
from ..ml.optimization import GeneticOptimizer
from ..experimental.synthesis_protocols import SynthesisProtocol
from ..experimental.characterization import CharacterizationSuite

# This is a simplified dependency injection setup.
# In a real application, you might use a more robust DI framework.

db_manager = DatabaseManager("sqlite:///./test.db")
materials_crud = MaterialsCRUD(db_manager.get_session())
experimental_crud = ExperimentalCRUD(db_manager.get_session())
property_predictor = PropertyPredictor()
genetic_optimizer = GeneticOptimizer()
synthesis_protocol_library = SynthesisProtocol()
characterization_suite = CharacterizationSuite()

def get_discovery_agent() -> MaterialsDiscoveryAgent:
    return MaterialsDiscoveryAgent(property_predictor, materials_crud)

def get_synthesis_agent() -> SynthesisAgent:
    return SynthesisAgent(synthesis_protocol_library, experimental_crud)

def get_characterization_agent() -> CharacterizationAgent:
    return CharacterizationAgent(characterization_suite, experimental_crud)

def get_optimization_agent() -> OptimizationAgent:
    return OptimizationAgent(genetic_optimizer)

def get_experimental_agent() -> ExperimentalAgent:
    return ExperimentalAgent()