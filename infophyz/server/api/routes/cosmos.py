from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

from infophyz.engine.cosmos.runner.cosmos_runner import (
    run_cosmos,
    run_cosmos_with_surgery
)

router = APIRouter()


# -----------------------------
# Request Models
# -----------------------------

class RunRequest(BaseModel):
    steps: int = 10


class SurgeryEvent(BaseModel):
    t: int
    event: Dict[str, Any]


class RunWithSurgeryRequest(BaseModel):
    steps: int = 10
    surgery_events: List[SurgeryEvent] = []


# -----------------------------
# Routes
# -----------------------------

@router.post("/run")
def run_cosmos_route(req: RunRequest):
    """
    Run the Info-Phys cosmos for N steps.
    """
    state = run_cosmos(req.steps)
    return {
        "status": "ok",
        "steps": req.steps,
        "state": state
    }


@router.post("/run_with_surgery")
def run_cosmos_with_surgery_route(req: RunWithSurgeryRequest):
    """
    Run the cosmos with scheduled surgery events.
    """
    events = [
        {"t": e.t, "event": e.event}
        for e in req.surgery_events
    ]

    state = run_cosmos_with_surgery(req.steps, events)

    return {
        "status": "ok",
        "steps": req.steps,
        "surgery_events": events,
        "state": state
    }