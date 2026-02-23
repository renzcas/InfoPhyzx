from typing import Dict
import math


def is_prime(n: int) -> bool:
    """Simple primality test."""
    if n < 2:
        return False
    if n % 2 == 0 and n != 2:
        return False
    r = int(math.sqrt(n))
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True


def prime_list(max_p: int) -> list:
    """Return all primes ≤ max_p."""
    return [p for p in range(2, max_p + 1) if is_prime(p)]


def prime_pulses(t: float, max_p: int = 50) -> Dict[int, float]:
    """
    Prime oscillatory forcing:
    f_p(t) = sin(t * log(p)) / sqrt(p)

    Returns a dict {prime: pulse_value}.
    """

    pulses = {}
    for p in prime_list(max_p):
        pulses[p] = math.sin(t * math.log(p)) / math.sqrt(p)
    return pulses