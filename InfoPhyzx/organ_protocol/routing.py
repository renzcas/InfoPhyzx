class Routing:
    def __init__(self, engine, pipeline, ui):
        self.engine = engine
        self.pipeline = pipeline
        self.ui = ui

    def handle_event(self, event):
        if event["type"] == "mutate_engine":
            self.engine.mutate(event["params"])

        if event["type"] == "set_scenario":
            self.pipeline.scenario(event["name"])

        return self.ui.receive_state()
