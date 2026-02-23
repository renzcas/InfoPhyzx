from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from infophyz.engine.cosmos.math.primes import prime_pulses
from infophyz.engine.cosmos.math.hilbert import hilbert_field, hilbert_energy
from infophyz.engine.cosmos.math.riemann import riemann_field, riemann_energy
from infophyz.engine.cosmos.math.ricci import clustering_curvature, average_curvature
from infophyz.engine.cosmos.math.perelman import edge_entropy, total_entropy

router = APIRouter()


# -----------------------------
# Request Models
# -----------------------------

class TimeRequest(BaseModel):
    t: float = 0.0
    N: int = 50
    L: int = 200


class GraphRequest(BaseModel):
    graph: Dict[str, Any]


# -----------------------------
# Routes
# -----------------------------

@router.post("/primes")
def primes_route(req: TimeRequest):
    """
    Return prime pulses at time t.
    """
    pulses = prime_pulses(req.t, max_p=req.N)
    return {
        "status": "ok",
        "t": req.t,
        "max_p": req.N,
        "pulses": pulses
    }


@router.post("/hilbert")
def hilbert_route(req: TimeRequest):
    """
    Return Hilbert field and energy at time t.
    """
    field = hilbert_field(req.t, N=req.N)
    energy = hilbert_energy(req.t, N=req.N)
    return {
        "status": "ok",
        "t": req.t,
        "N": req.N,
        "field": field,
        "energy": energy
    }


@router.post("/riemann")
def riemann_route(req: TimeRequest):
    """
    Return Riemann spectral field and energy at time t.
    """
    field = riemann_field(req.t, L=req.L)
    energy = riemann_energy(req.t, L=req.L)
    return {
        "status": "ok",
        "t": req.t,
        "L": req.L,
        "field": field,
        "energy": energy
    }


@router.post("/curvature")
def curvature_route(req: GraphRequest):
    """
    Compute clustering curvature for a graph.
    """
    K = clustering_curvature(req.graph)
    avg = average_curvature(req.graph)
    return {
        "status": "ok",
        "curvature": K,
        "average": avg
    }


@router.post("/entropy")
def entropy_route(req: GraphRequest):
    """
    Compute Perelman-style edge entropy for a graph.
    """
    S = edge_entropy(req.graph)
    total = total_entropy(req.graph)
    return {
        "status": "ok",
        "entropy": S,
        "total": total
    }