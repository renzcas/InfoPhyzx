class Orchestrator:
    def __init__(self, engine, pipeline, ui, adapters):
        self.engine = engine
        self.pipeline = pipeline
        self.ui = ui
        self.adapters = adapters

    def step(self):
        self.engine.step()
        pipeline_output = self.adapters["engine_to_pipeline"].tick()
        self.adapters["pipeline_to_ui"].update_ui()
        return pipeline_output

    def run(self, ticks=1):
        for _ in range(ticks):
            self.step()
