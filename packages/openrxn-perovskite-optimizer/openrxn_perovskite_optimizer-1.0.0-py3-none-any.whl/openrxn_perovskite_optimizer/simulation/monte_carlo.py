import numpy as np

class MonteCarloSimulator:
    """Performs Monte Carlo simulations to assess property distributions."""
    def __init__(self, n_samples: int = 1000):
        self.n_samples = n_samples

    def run_simulation(self, property_mean, property_std):
        """Runs a Monte Carlo simulation for a given property."""
        samples = np.random.normal(property_mean, property_std, self.n_samples)
        return {
            "mean": np.mean(samples),
            "std": np.std(samples),
            "samples": samples.tolist(),
        }