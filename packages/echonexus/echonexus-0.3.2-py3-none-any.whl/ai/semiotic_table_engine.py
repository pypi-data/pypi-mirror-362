class SemioticTableEngine:
    """Simple registry mapping components to symbolic roles.

    The engine provides a lightweight interface for registering and
    retrieving symbolic roles tied to components such as RedStone or
    EchoNode. It can be extended to persist or synchronize mappings.
    """

    def __init__(self):
        self.registry = {}

    def register(self, component, roles):
        """Register a component with its symbolic roles."""
        self.registry[component] = list(roles)

    def get_roles(self, component):
        return self.registry.get(component, [])

    def all_components(self):
        return list(self.registry.keys())
