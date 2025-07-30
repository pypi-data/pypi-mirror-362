class Resolver:
    """
    Resolves a Python class path
    """

    def __call__(self, path):
        """
        Class instance to resolve.

        Args:
            path: path to class

        Returns:
            class instance
        """

        parts = path.split(".")

        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)

        return m
