class PipelineToUIAdapter:
    def __init__(self, pipeline, ui):
        self.pipeline = pipeline
        self.ui = ui

    def update_ui(self):
        output = self.pipeline.flow()
        return self.ui.send_event({"pipeline_output": output})
