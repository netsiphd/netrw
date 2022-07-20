class BaseRewirer:
    """
    Base class for rewiring algorithms.

    All rewiring algorithms should inherit from this class.

    """

    def __init__(self):
        return

    def __call__(self, *args, **kwargs):
        return self.full_rewire(*args, **kwargs)

    # For all rewiring, whether the algorithm is iterative or not. "full" refers to rewiring until an end condition.
    def full_rewire(self, G, **kwargs):
        raise NotImplementedError

    # For rewiring algorithms that can implemented iteratively. Iterative algorithms should also implement full_rewire.
    def step_rewire(self, G, **kwargs):
        raise NotImplementedError
