import math
from typing import List


def hilbert_mode(n: int, t: float) -> float:
    """
    A single Hilbert mode:
    h_n(t) = sin(n * t) / n

    Smooth, decaying harmonic oscillation.
    """
    if n <= 0:
        return 0.0
    return math.sin(n * t) / n


def hilbert_field(t: float, N: int = 50) -> List[float]:
    """
    Compute the first N Hilbert modes at time t.
    Returns a list [h_1(t), h_2(t), ..., h_N(t)].
    """
    return [hilbert_mode(n, t) for n in range(1, N + 1)]


def hilbert_energy(t: float, N: int = 50) -> float:
    """
    Total Hilbert energy:
    E(t) = sum |h_n(t)|

    Smooth forcing term for the cosmos.
    """
    return sum(abs(hilbert_mode(n, t)) for n in range(1, N + 1))