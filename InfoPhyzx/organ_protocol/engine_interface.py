class EngineInterface:
    """
    Contract for the Cosmos Engine organism.
    Defines the physics-level operations that must be exposed.
    """

    def simulate(self, steps: int):
        """Run the engine for N steps."""
        raise NotImplementedError

    def step(self):
        """Advance the engine by one tick."""
        raise NotImplementedError

    def mutate(self, params: dict):
        """Apply mutations or parameter changes to the engine."""
        raise NotImplementedError

    def get_dimensions(self) -> tuple:
        """Return the spatial/temporal dimensions of the engine."""
        raise NotImplementedError

    def get_energy(self) -> float:
        """Return the current energy state of the system."""
        raise NotImplementedError
