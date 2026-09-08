"""Analytics queries for historical flight-price observations."""

from __future__ import annotations

from typing import Any

from database import FlightDatabase


class FlightAnalytics:
    """Provide dashboard-ready metrics from the MySQL price history."""

    def __init__(self, database: FlightDatabase) -> None:
        self.database = database

    def routes(self) -> list[dict[str, str]]:
        """Return unique origin/destination pairs available in the history."""
        query = """
        SELECT DISTINCT origin, destination
        FROM flight_prices
        ORDER BY origin, destination
        """
        with self.database.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
        return [{"origin": str(row["origin"]), "destination": str(row["destination"])} for row in rows]

    def lowest_price(self, origin: str | None = None, destination: str | None = None) -> float | None:
        query = "SELECT MIN(price) AS lowest_price FROM flight_prices"
        conditions: list[str] = []
        values: list[Any] = []
        if origin:
            conditions.append("origin = %s")
            values.append(origin.upper())
        if destination:
            conditions.append("destination = %s")
            values.append(destination.upper())
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        with self.database.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, tuple(values))
            row = cursor.fetchone()
            cursor.close()
        return float(row["lowest_price"]) if row and row["lowest_price"] is not None else None

    def average_price(self, origin: str | None = None, destination: str | None = None) -> float | None:
        query = "SELECT AVG(price) AS average_price FROM flight_prices"
        conditions: list[str] = []
        values: list[Any] = []
        if origin:
            conditions.append("origin = %s")
            values.append(origin.upper())
        if destination:
            conditions.append("destination = %s")
            values.append(destination.upper())
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        with self.database.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, tuple(values))
            row = cursor.fetchone()
            cursor.close()
        return float(row["average_price"]) if row and row["average_price"] is not None else None

    def latest_price(self, origin: str, destination: str) -> float | None:
        query = """
        SELECT price FROM flight_prices
        WHERE origin = %s AND destination = %s
        ORDER BY searched_at DESC, id DESC LIMIT 1
        """
        with self.database.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (origin.upper(), destination.upper()))
            row = cursor.fetchone()
            cursor.close()
        return float(row["price"]) if row else None

    def price_trend(self, origin: str, destination: str, limit: int = 100) -> list[dict[str, Any]]:
        """Return chronological observations for a Plotly time-series chart."""
        if limit <= 0:
            raise ValueError("limit must be greater than zero")
        query = """
        SELECT searched_at, price, airline, stops, departure_date
        FROM flight_prices
        WHERE origin = %s AND destination = %s
        ORDER BY searched_at DESC, id DESC LIMIT %s
        """
        with self.database.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (origin.upper(), destination.upper(), limit))
            rows = cursor.fetchall()
            cursor.close()
        return list(reversed(rows))

    def cheapest_destinations(self, origin: str, limit: int = 10) -> list[dict[str, Any]]:
        """Return destinations ranked by historical minimum fare."""
        if limit <= 0:
            raise ValueError("limit must be greater than zero")
        query = """
        SELECT destination, MIN(price) AS lowest_price, AVG(price) AS average_price
        FROM flight_prices WHERE origin = %s
        GROUP BY destination ORDER BY lowest_price ASC LIMIT %s
        """
        with self.database.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (origin.upper(), limit))
            rows = cursor.fetchall()
            cursor.close()
        return list(rows)

    def target_vs_actual(self, origin: str, destination: str) -> dict[str, float | None]:
        """Compare the latest observed fare with the latest stored target price."""
        query = """
        SELECT price, target_price FROM flight_prices
        WHERE origin = %s AND destination = %s
        ORDER BY searched_at DESC, id DESC LIMIT 1
        """
        with self.database.connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (origin.upper(), destination.upper()))
            row = cursor.fetchone()
            cursor.close()
        if not row:
            return {"actual": None, "target": None, "variance": None}
        actual = float(row["price"])
        target = float(row["target_price"]) if row["target_price"] is not None else None
        return {"actual": actual, "target": target, "variance": actual - target if target is not None else None}
