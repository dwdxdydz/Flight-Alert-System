from unittest.mock import MagicMock

import pytest

from analytics import FlightAnalytics


def make_database(rows):
    database = MagicMock()
    connection = database.connection.return_value.__enter__.return_value
    cursor = connection.cursor.return_value
    cursor.fetchone.return_value = rows[0] if rows else None
    cursor.fetchall.return_value = rows
    return database, cursor


def test_lowest_price():
    database, cursor = make_database([{"lowest_price": 125.5}])
    analytics = FlightAnalytics(database)

    assert analytics.lowest_price("BLR", "AMS") == 125.5
    cursor.execute.assert_called_once()


def test_average_price():
    database, _ = make_database([{"average_price": 250.0}])
    analytics = FlightAnalytics(database)

    assert analytics.average_price("BLR", "AMS") == 250.0


def test_latest_price():
    database, _ = make_database([{"price": 199.0}])
    analytics = FlightAnalytics(database)

    assert analytics.latest_price("BLR", "AMS") == 199.0


def test_price_trend_is_chronological():
    rows = [
        {"searched_at": "2026-09-02", "price": 300},
        {"searched_at": "2026-09-01", "price": 250},
    ]
    database, _ = make_database(rows)
    analytics = FlightAnalytics(database)

    result = analytics.price_trend("BLR", "AMS")

    assert result[0]["searched_at"] == "2026-09-02"
    assert result[1]["searched_at"] == "2026-09-01"


def test_limit_validation():
    database, _ = make_database([])
    analytics = FlightAnalytics(database)

    with pytest.raises(ValueError):
        analytics.price_trend("BLR", "AMS", 0)

    with pytest.raises(ValueError):
        analytics.cheapest_destinations("BLR", 0)


def test_target_vs_actual():
    database, _ = make_database([{"price": 380.0, "target_price": 400.0}])
    analytics = FlightAnalytics(database)

    assert analytics.target_vs_actual("BLR", "AMS") == {
        "actual": 380.0,
        "target": 400.0,
        "variance": -20.0,
    }


def test_target_vs_actual_without_history():
    database, _ = make_database([])
    analytics = FlightAnalytics(database)

    assert analytics.target_vs_actual("BLR", "AMS") == {
        "actual": None,
        "target": None,
        "variance": None,
    }
