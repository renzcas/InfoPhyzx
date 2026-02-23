from typing import Callable, Tuple, TypeVar, Generic

S = TypeVar("S")  # State type
A = TypeVar("A")  # Output type

class State(Generic[S, A]):
    """
    A simple State monad:
    - run: (state) -> (value, new_state)
    """

    def __init__(self, run: Callable[[S], Tuple[A, S]]):
        self.run = run

    def map(self, f: Callable[[A], A]):
        """Transforms the output value but not the state."""
        def new_run(state: S):
            (value, new_state) = self.run(state)
            return (f(value), new_state)
        return State(new_run)

    def bind(self, f: Callable[[A], "State[S, A]"]):
        """Chains stateful computations."""
        def new_run(state: S):
            (value, new_state) = self.run(state)
            return f(value).run(new_state)
        return State(new_run)

    @staticmethod
    def pure(x: A):
        """Wraps a value into a State monad without changing state."""
        return State(lambda s: (x, s))