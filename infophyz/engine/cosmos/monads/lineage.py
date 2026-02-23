from typing import Dict, Any, Tuple, List
from .state import State


def init_lineage_if_missing(state: Dict[str, Any]):
    """Ensure lineage structure exists."""
    if "lineage" not in state:
        state["lineage"] = {}
    for n in state["graph"]["nodes"]:
        if n not in state["lineage"]:
            state["lineage"][n] = {
                "parents": [],
                "children": [],
                "events": []
            }


def record_event(node: str, event: Dict[str, Any]) -> None:
    """Append an event to a node's lineage."""
    event_list: List[Dict[str, Any]] = event.get("events", [])
    event_list.append(event)


def lineage_split(parent: str, child: str) -> State[Dict[str, Any], None]:
    """
    Record that a node split into a new child node.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        init_lineage_if_missing(state)

        lineage = state["lineage"]

        # Ensure entries exist
        if parent not in lineage:
            lineage[parent] = {"parents": [], "children": [], "events": []}
        if child not in lineage:
            lineage[child] = {"parents": [], "children": [], "events": []}

        # Update relationships
        lineage[parent]["children"].append(child)
        lineage[child]["parents"].append(parent)

        # Log event
        event = {
            "type": "lineage_split",
            "parent": parent,
            "child": child
        }
        lineage[parent]["events"].append(event)
        lineage[child]["events"].append(event)

        state["log"].append(event)

        return (None, state)

    return State(run)


def lineage_merge(a: str, b: str, survivor: str) -> State[Dict[str, Any], None]:
    """
    Record that two nodes merged into a survivor.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        init_lineage_if_missing(state)

        lineage = state["lineage"]

        for n in [a, b, survivor]:
            if n not in lineage:
                lineage[n] = {"parents": [], "children": [], "events": []}

        # Update relationships
        lineage[a]["children"].append(survivor)
        lineage[b]["children"].append(survivor)
        lineage[survivor]["parents"].extend([a, b])

        # Log event
        event = {
            "type": "lineage_merge",
            "a": a,
            "b": b,
            "survivor": survivor
        }
        lineage[a]["events"].append(event)
        lineage[b]["events"].append(event)
        lineage[survivor]["events"].append(event)

        state["log"].append(event)

        return (None, state)

    return State(run)


def lineage_birth(node: str) -> State[Dict[str, Any], None]:
    """
    Record that a node was born with no parents.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        init_lineage_if_missing(state)

        lineage = state["lineage"]

        if node not in lineage:
            lineage[node] = {"parents": [], "children": [], "events": []}

        event = {
            "type": "lineage_birth",
            "node": node
        }
        lineage[node]["events"].append(event)
        state["log"].append(event)

        return (None, state)

    return State(run)


def lineage_death(node: str) -> State[Dict[str, Any], None]:
    """
    Record that a node died.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        init_lineage_if_missing(state)

        lineage = state["lineage"]

        if node not in lineage:
            lineage[node] = {"parents": [], "children": [], "events": []}

        event = {
            "type": "lineage_death",
            "node": node
        }
        lineage[node]["events"].append(event)
        state["log"].append(event)

        return (None, state)

    return State(run)