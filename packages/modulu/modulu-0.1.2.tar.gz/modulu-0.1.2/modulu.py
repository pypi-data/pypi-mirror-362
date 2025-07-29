class Modulu:
    """
    Modulu represents a simple numeric value with utility methods.
    """
    def __init__(self, value: float):
        """
        Initialize Modulu with a numeric value.

        Args:
            value (float): The initial value.
        """
        self.value = value

    def double(self) -> float:
        """
        Returns the value multiplied by 2.

        Returns:
            float: Double the value.
        """
        return self.value * 2

    def triple(self) -> float:
        """
        Returns the value multiplied by 3.

        Returns:
            float: Triple the value.
        """
        return self.value * 3

    def increment(self, amount: float = 1.0) -> None:
        """
        Increments the value by a specified amount.

        Args:
            amount (float, optional): Amount to increment. Defaults to 1.0.
        """
        self.value += amount

    def __repr__(self) -> str:
        return f"Modulu(value={self.value})"

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation.
        """
        return f"Modulu with value {self.value}"

__version__ = "0.1.2"
