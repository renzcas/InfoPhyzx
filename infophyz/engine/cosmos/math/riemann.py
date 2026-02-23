import math
from typing import List


def riemann_mode(t: float, n: int) -> float:
    """
    A simple Riemann-inspired spectral mode:
    R_n(t) = cos(t * log(n)) / sqrt(n)

    This mimics the oscillatory structure of terms appearing
    in explicit formulas related to the zeta function.
    """
    if n <= 1:
        return 0.0
    return math.cos(t * math.log(n)) / math.sqrt(n)


def riemann_field(t: float, L: int = 200) -> List[float]:
    """
    Compute the first L Riemann spectral modes.
    Returns a list [R_2(t), R_3(t), ..., R_{L+1}(t)].
    """
    return [riemann_mode(t, n) for n in range(2, L + 2)]


def riemann_energy(t: float, L: int = 200) -> float:
    """
    Total Riemann spectral energy:
    E(t) = sum |R_n(t)|

    This is used as a forcing term in the Info-Phys flow.
    """
    return sum(abs(riemann_mode(t, n)) for n in range(2, L + 2))