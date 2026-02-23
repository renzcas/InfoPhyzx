from typing import Dict, Any
import math


def edge_entropy(graph: Dict[str, Any]) -> Dict[tuple, float]:
    """
    Perelman-inspired edge entropy.

    For each edge (u, v) with weight w:
        S(u, v) = - w * log(w)

    This measures local disorder.
    """

    edges = graph["edges"]
    entropy = {}

    for (u, v), w in edges.items():
        if w <= 0:
            entropy[(u, v)] = 0.0
        else:
            entropy[(u, v)] = -w * math.log(w)

    return entropy


def total_entropy(graph: Dict[str, Any]) -> float:
    """
    Total Perelman-style entropy across all edges.
    """
    S = edge_entropy(graph)
    return sum(S.values())