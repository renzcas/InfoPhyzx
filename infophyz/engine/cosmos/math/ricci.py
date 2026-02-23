from typing import Dict, Any
import math


def clustering_curvature(graph: Dict[str, Any]) -> Dict[str, float]:
    """
    A simple Ricci-like curvature measure based on local clustering.

    For each node:
        K(v) = (# of triangles touching v) / (degree(v) choose 2)

    If degree < 2, curvature = 0.
    """

    nodes = graph["nodes"]
    edges = graph["edges"]

    # Build adjacency list
    adj = {n: set() for n in nodes}
    for (u, v) in edges:
        adj[u].add(v)
        adj[v].add(u)

    curvature = {}

    for v in nodes:
        neighbors = list(adj[v])
        d = len(neighbors)

        if d < 2:
            curvature[v] = 0.0
            continue

        # Count triangles
        triangles = 0
        for i in range(d):
            for j in range(i + 1, d):
                a = neighbors[i]
                b = neighbors[j]
                if (a, b) in edges or (b, a) in edges:
                    triangles += 1

        # Max possible triangles
        max_tri = d * (d - 1) / 2
        curvature[v] = triangles / max_tri if max_tri > 0 else 0.0

    return curvature


def average_curvature(graph: Dict[str, Any]) -> float:
    """
    Average curvature across all nodes.
    """
    K = clustering_curvature(graph)
    if len(K) == 0:
        return 0.0
    return sum(K.values()) / len(K)