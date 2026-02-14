from organ_protocol.pipeline_interface import PipelineInterface

class PipelineWrapper(PipelineInterface):
    def __init__(self, pipeline_impl):
        self.pipeline = pipeline_impl

    def ingest(self, data):
        return self.pipeline.ingest(data)

    def transform(self):
        return self.pipeline.transform()

    def scenario(self, name: str):
        return self.pipeline.scenario(name)

    def flow(self):
        return self.pipeline.flow()
