class NudgeRegistry:
    """Simple registry to track nudges for testing purposes."""
    def __init__(self):
        self.nudges = []

    def register(self, nudge):
        self.nudges.append(nudge)

    def all_nudges(self):
        return list(self.nudges)
