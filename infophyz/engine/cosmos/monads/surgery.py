from typing import Dict, Any, Tuple
from .state import State
import random


def split_node(node: str) -> State[Dict[str, Any], None]:
    """
    Split a node into two nodes:
    - new node gets half of the edges
    - original node keeps the other half
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        graph = state["graph"]
        edges = graph["edges"]

        # Create new node
        new_node = f"{node}_split_{random.randint(1000,9999)}"
        graph["nodes"].append(new_node)

        # Partition edges
        connected = [(u, v) for (u, v) in edges if u == node or v == node]
        half = len(connected) // 2

        for (u, v) in connected[:half]:
            w = edges.pop((u, v))
            # Reassign to new node
            if u == node:
                edges[(new_node, v)] = w
            else:
                edges[(u, new_node)] = w

        # Log
        state["log"].append({
            "type": "surgery_split",
            "original": node,
            "new": new_node,
            "edges_moved": half
        })

        return (None, state)

    return State(run)


def merge_nodes(a: str, b: str) -> State[Dict[str, Any], None]:
    """
    Merge two nodes into a single node.
    All edges are redirected to the surviving node.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        graph = state["graph"]
        edges = graph["edges"]

        survivor = a
        removed = b

        # Redirect edges
        new_edges = {}
        for (u, v), w in edges.items():
            if u == removed:
                u = survivor
            if v == removed:
                v = survivor
            if u != v:
                new_edges[(u, v)] = w

        edges.clear()
        edges.update(new_edges)

        # Remove node
        if removed in graph["nodes"]:
            graph["nodes"].remove(removed)

        # Log
        state["log"].append({
            "type": "surgery_merge",
            "survivor": survivor,
            "removed": removed
        })

        return (None, state)

    return State(run)


def collapse_edge(u: str, v: str) -> State[Dict[str, Any], None]:
    """
    Remove an edge entirely.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        graph = state["graph"]
        edges = graph["edges"]

        if (u, v) in edges:
            edges.pop((u, v))

        state["log"].append({
            "type": "surgery_collapse_edge",
            "edge": (u, v)
        })

        return (None, state)

    return State(run)


def birth_node(name: str) -> State[Dict[str, Any], None]:
    """
    Create a new isolated node.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        graph = state["graph"]

        if name not in graph["nodes"]:
            graph["nodes"].append(name)

        state["log"].append({
            "type": "surgery_birth",
            "node": name
        })

        return (None, state)

    return State(run)


def death_node(name: str) -> State[Dict[str, Any], None]:
    """
    Remove a node and all its edges.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        graph = state["graph"]
        edges = graph["edges"]

        if name in graph["nodes"]:
            graph["nodes"].remove(name)

        # Remove edges touching the node
        edges_to_remove = [(u, v) for (u, v) in edges if u == name or v == name]
        for e in edges_to_remove:
            edges.pop(e)

        state["log"].append({
            "type": "surgery_death",
            "node": name,
            "edges_removed": len(edges_to_remove)
        })

        return (None, state)

    return State(run)