from typing import Dict, Any, Tuple
from .state import State

from infophyz.engine.cosmos.math.primes import prime_pulses
from infophyz.engine.cosmos.math.riemann import riemann_energy
from infophyz.engine.cosmos.math.ricci import clustering_curvature
from infophyz.engine.cosmos.math.perelman import edge_entropy


def flow_step(alpha: float = 0.1, beta: float = 0.1, t: float = 0.0) -> State[Dict[str, Any], None]:
    """
    Ricci-like flow step with:
    - curvature (clustering-based)
    - entropy (edge-based)
    - prime forcing
    - Riemann spectral forcing

    Returns a State monad that updates the cosmos graph.
    """

    def run(state: Dict[str, Any]) -> Tuple[None, Dict[str, Any]]:
        graph = state["graph"]
        edges = graph["edges"]

        # --- Compute geometric quantities ---
        K = clustering_curvature(graph)
        S = edge_entropy(graph)

        # --- Number-theoretic forcing ---
        P = prime_pulses(t, max_p=50)
        prime_energy = sum(abs(v) for v in P.values())

        # --- Riemann spectral forcing ---
        R = riemann_energy(t, L=200)

        # --- Update edges ---
        new_edges = {}

        for (u, v), w in edges.items():
            dK = K[u] - K[v]
            dS = S[(u, v)]

            forcing_prime = 0.02 * prime_energy
            forcing_riemann = 0.03 * R

            w_new = (
                w
                + alpha * (-abs(dK))     # curvature smoothing
                + beta * (-dS)           # entropy smoothing
                + forcing_prime          # prime forcing
                + forcing_riemann        # Riemann forcing
            )

            w_new = max(w_new, 0.01)
            new_edges[(u, v)] = w_new

        graph["edges"] = new_edges

        # --- Log the flow step ---
        state["log"].append({
            "type": "flow",
            "t": t,
            "curvature": K,
            "entropy": S,
            "prime_energy": prime_energy,
            "riemann_energy": R,
            "reaction_prime": forcing_prime,
            "reaction_riemann": forcing_riemann,
            "edges": new_edges.copy()
        })

        return (None, state)

    return State(run)