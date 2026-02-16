class PipelineInterface:
    """
    Contract for the Pipeline Engine organism.
    Defines the dataflow and transformation operations.
    """

    def ingest(self, data):
        """Receive raw data or state from another organism."""
        raise NotImplementedError

    def transform(self):
        """Apply transformations to the ingested data."""
        raise NotImplementedError

    def scenario(self, name: str):
        """Switch pipeline behavior based on scenario name."""
        raise NotImplementedError

    def flow(self):
        """Execute the pipeline flow and return output."""
        raise NotImplementedError
