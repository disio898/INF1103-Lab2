from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy interface: every discount offers the same apply() method."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the total after the discount has been applied."""


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off the total, e.g. PercentageDiscount(10) = 10% off."""

    def __init__(self, percentage: float) -> None:
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Takes `amount` off any total that reaches `threshold`."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.threshold: float = threshold
        self.amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return max(total - self.amount, 0.0)
        return total


class StudentDiscount(PercentageDiscount):
    """Fourth strategy (Section 2.4): a fixed 5% student discount.

    Added without touching Order or any other strategy.
    """

    def __init__(self) -> None:
        super().__init__(5)