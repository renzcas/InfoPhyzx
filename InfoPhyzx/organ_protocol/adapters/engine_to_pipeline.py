class EngineToPipelineAdapter:
    def __init__(self, engine, pipeline):
        self.engine = engine
        self.pipeline = pipeline

    def tick(self):
        state = {
            "energy": self.engine.get_energy(),
            "dimensions": self.engine.get_dimensions()
        }
        self.pipeline.ingest(state)
        return self.pipeline.flow()
