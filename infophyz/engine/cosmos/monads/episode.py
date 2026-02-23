from typing import Dict, Any, Tuple, List
from .state import State
from .flow import flow_step
from .meta import meta_step
from .surgery import (
    split_node, merge_nodes, collapse_edge,
    birth_node, death_node
)
from .lineage import (
    lineage_split, lineage_merge,
    lineage_birth, lineage_death
)


def episode_step(t: float) -> State[Dict[str, Any], None]:
    """
    A full Info-Phys episode step:
    1. Flow update (Ricci + entropy + forcing)
    2. Meta update (Perelman-style parameter evolution)
    3. Optional surgery events
    4. Lineage updates
    5. Logging

    All wrapped in a State monad for deterministic replay.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        # --- 1. FLOW ---
        (_, state) = flow_step(
            alpha=state["params"]["alpha"],
            beta=state["params"]["beta"],
            t=t
        ).run(state)

        # --- 2. META ---
        (_, state) = meta_step().run(state)

        # --- 3. SURGERY EVENTS ---
        surgeries: List[Dict[str, Any]] = state.get("pending_surgery", [])

        for event in surgeries:
            etype = event["type"]

            if etype == "split":
                node = event["node"]
                (_, state) = split_node(node).run(state)
                (_, state) = lineage_split(node, f"{node}_child").run(state)

            elif etype == "merge":
                a = event["a"]
                b = event["b"]
                survivor = event["survivor"]
                (_, state) = merge_nodes(a, b).run(state)
                (_, state) = lineage_merge(a, b, survivor).run(state)

            elif etype == "collapse_edge":
                u, v = event["u"], event["v"]
                (_, state) = collapse_edge(u, v).run(state)

            elif etype == "birth":
                node = event["node"]
                (_, state) = birth_node(node).run(state)
                (_, state) = lineage_birth(node).run(state)

            elif etype == "death":
                node = event["node"]
                (_, state) = death_node(node).run(state)
                (_, state) = lineage_death(node).run(state)

        # Clear surgery queue
        state["pending_surgery"] = []

        # --- 4. LOG EPISODE ---
        state["log"].append({
            "type": "episode",
            "t": t,
            "alpha": state["params"]["alpha"],
            "beta": state["params"]["beta"],
            "nodes": list(state["graph"]["nodes"]),
            "edges": dict(state["graph"]["edges"])
        })

        return (None, state)

    return State(run)