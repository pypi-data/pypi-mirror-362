class Modulu:
    def __init__(self, value):
        self.value = value

    def double(self):
        return self.value * 2

    def triple(self):
        """Returns the value multiplied by 3."""
        return self.value * 3

    def __repr__(self):
        return f"Modulu(value={self.value})"
