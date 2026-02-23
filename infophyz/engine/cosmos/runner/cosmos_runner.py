from typing import Dict, Any, List
from infophyz.engine.cosmos.monads.episode import episode_step


def init_cosmos() -> Dict[str, Any]:
    """
    Initialize a minimal cosmos state.
    This can be replaced later with loaders or scenario files.
    """

    return {
        "graph": {
            "nodes": ["A", "B", "C"],
            "edges": {
                ("A", "B"): 1.0,
                ("B", "C"): 1.0,
                ("A", "C"): 1.0
            }
        },
        "params": {
            "alpha": 0.1,
            "beta": 0.1
        },
        "pending_surgery": [],
        "lineage": {},
        "log": []
    }


def run_cosmos(steps: int = 10) -> Dict[str, Any]:
    """
    Run N episodes of the Info-Phys cosmos.
    Returns the full state including logs.
    """

    state = init_cosmos()

    for t in range(steps):
        (_, state) = episode_step(t).run(state)

    return state


def run_cosmos_with_surgery(steps: int, surgery_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Run N episodes but inject surgery events at specific times.
    surgery_events = [
        {"t": 3, "event": {"type": "split", "node": "A"}},
        {"t": 7, "event": {"type": "merge", "a": "B", "b": "C", "survivor": "BC"}}
    ]
    """

    state = init_cosmos()

    # Organize events by time
    events_by_t = {}
    for e in surgery_events:
        t = e["t"]
        if t not in events_by_t:
            events_by_t[t] = []
        events_by_t[t].append(e["event"])

    for t in range(steps):
        # Inject events for this timestep
        if t in events_by_t:
            state["pending_surgery"].extend(events_by_t[t])

        (_, state) = episode_step(t).run(state)

    return state