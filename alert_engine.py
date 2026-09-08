"""Business rules for deciding when a flight-price alert is valuable."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlertDecision:
    """Explain why a flight should or should not trigger an alert."""

    should_alert: bool
    reasons: tuple[str, ...] = ()


class AlertEngine:
    """Evaluate target, price-drop and historical-low alert rules."""

    def __init__(self, significant_drop_percent: float = 10.0) -> None:
        if significant_drop_percent <= 0:
            raise ValueError("significant_drop_percent must be greater than zero")
        self.significant_drop_percent = significant_drop_percent

    def evaluate(
        self,
        current_price: float,
        target_price: float,
        previous_price: float | None = None,
        previous_lowest_price: float | None = None,
    ) -> AlertDecision:
        reasons: list[str] = []

        if current_price <= target_price:
            reasons.append("target price reached")

        if previous_price and previous_price > 0:
            drop_percent = ((previous_price - current_price) / previous_price) * 100
            if drop_percent >= self.significant_drop_percent:
                reasons.append(f"price dropped {drop_percent:.1f}%")

        if previous_lowest_price is not None and current_price < previous_lowest_price:
            reasons.append("new historical low")

        return AlertDecision(bool(reasons), tuple(reasons))
