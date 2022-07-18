class BaseRewirer:
    """
    Base class for rewiring algorithms.

    All rewiring algorithms should inherit from this class.

    """

    def __init__(self):
        return

    def __call__(self, *args, **kwargs):
        return self.rewire(*args, **kwargs)

    def rewire(self, G, **kwargs):
        return G
