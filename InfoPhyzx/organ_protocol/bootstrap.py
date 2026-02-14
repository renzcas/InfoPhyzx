from organ_protocol.wrappers.engine_wrapper import EngineWrapper
from organ_protocol.wrappers.pipeline_wrapper import PipelineWrapper
from organ_protocol.wrappers.ui_wrapper import UIWrapper

from organ_protocol.adapters.engine_to_pipeline import EngineToPipelineAdapter
from organ_protocol.adapters.pipeline_to_ui import PipelineToUIAdapter

from organ_protocol.orchestrator import Orchestrator
from organ_protocol.heartbeat import Heartbeat
from organ_protocol.routing import Routing

def bootstrap(engine_impl, pipeline_impl, ui_impl):
    engine = EngineWrapper(engine_impl)
    pipeline = PipelineWrapper(pipeline_impl)
    ui = UIWrapper(ui_impl)

    adapters = {
        "engine_to_pipeline": EngineToPipelineAdapter(engine, pipeline),
        "pipeline_to_ui": PipelineToUIAdapter(pipeline, ui)
    }

    orchestrator = Orchestrator(engine, pipeline, ui, adapters)
    routing = Routing(engine, pipeline, ui)
    heartbeat = Heartbeat(orchestrator)

    return {
        "engine": engine,
        "pipeline": pipeline,
        "ui": ui,
        "orchestrator": orchestrator,
        "routing": routing,
        "heartbeat": heartbeat
    }
