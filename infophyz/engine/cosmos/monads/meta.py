from typing import Dict, Any, Tuple
from .state import State

from infophyz.engine.cosmos.math.ricci import average_curvature
from infophyz.engine.cosmos.math.perelman import total_entropy


def meta_step() -> State[Dict[str, Any], None]:
    """
    Meta-director:
    Adjusts flow parameters (alpha, beta) based on global geometry.

    Inspired by Perelman's functionals:
    - If curvature is too high → increase smoothing
    - If entropy collapses → increase entropy weight
    - If system is stable → relax parameters
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        graph = state["graph"]
        params = state["params"]

        alpha = params.get("alpha", 0.1)
        beta = params.get("beta", 0.1)

        # --- Global geometric signals ---
        K_avg = average_curvature(graph)
        S_total = total_entropy(graph)

        # --- Meta adjustments ---
        if K_avg > 0.5:
            alpha *= 1.10   # more curvature smoothing
        elif K_avg < 0.1:
            alpha *= 0.95   # relax smoothing

        if S_total < 0.2:
            beta *= 1.15    # entropy collapse → strengthen entropy term
        elif S_total > 1.0:
            beta *= 0.90    # entropy too high → relax

        # Clamp to safe ranges
        alpha = max(0.01, min(alpha, 1.0))
        beta = max(0.01, min(beta, 1.0))

        # Update parameters
        params["alpha"] = alpha
        params["beta"] = beta

        # Log meta decision
        state["log"].append({
            "type": "meta",
            "alpha": alpha,
            "beta": beta,
            "avg_curvature": K_avg,
            "total_entropy": S_total
        })

        return (None, state)

    return State(run)