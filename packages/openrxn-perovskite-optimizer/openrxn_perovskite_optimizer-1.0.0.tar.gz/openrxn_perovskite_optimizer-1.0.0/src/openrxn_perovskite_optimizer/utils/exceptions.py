class OpenRXNError(Exception):
    """Base exception class for the OpenRXN platform."""
    pass

class DiscoveryError(OpenRXNError):
    """Exception raised for errors in the discovery agent."""
    pass

class SynthesisError(OpenRXNError):
    """Exception raised for errors in the synthesis agent."""
    pass

class CharacterizationError(OpenRXNError):
    """Exception raised for errors in the characterization agent."""
    pass

class OptimizationError(OpenRXNError):
    """Exception raised for errors in the optimization agent."""
    pass

class SimulationError(OpenRXNError):
    """Exception raised for errors in the simulation modules."""
    pass