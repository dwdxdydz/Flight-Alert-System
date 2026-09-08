"""MySQL persistence layer for historical flight price observations."""

from __future__ import annotations

import os
from contextlib import contextmanager
from datetime import datetime
from typing import Iterator

import mysql.connector
from mysql.connector import Error

from flight_data import FlightData


class DatabaseError(RuntimeError):
    """Raised when a database operation cannot be completed."""


class FlightDatabase:
    """Store and query historical flight-price observations in MySQL."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str | None = None,
    ) -> None:
        self.config = {
            "host": host or os.getenv("MYSQL_HOST", "127.0.0.1"),
            "port": port or int(os.getenv("MYSQL_PORT", "3306")),
            "user": user or os.getenv("MYSQL_USER", "root"),
            "password": password or os.getenv("MYSQL_PASSWORD", ""),
            "database": database or os.getenv("MYSQL_DATABASE", "flight_alert"),
        }

    @contextmanager
    def connection(self) -> Iterator[mysql.connector.MySQLConnection]:
        connection = None
        try:
            connection = mysql.connector.connect(**self.config)
            yield connection
        except Error as error:
            raise DatabaseError(f"MySQL operation failed: {error}") from error
        finally:
            if connection and connection.is_connected():
                connection.close()

    def initialize(self) -> None:
        """Create the historical observations table when it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS flight_prices (
            id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            searched_at DATETIME NOT NULL,
            origin VARCHAR(10) NOT NULL,
            destination VARCHAR(10) NOT NULL,
            departure_date DATE NOT NULL,
            return_date DATE NULL,
            airline VARCHAR(120) NULL,
            stops TINYINT UNSIGNED NOT NULL DEFAULT 0,
            price DECIMAL(12, 2) NOT NULL,
            currency CHAR(3) NOT NULL DEFAULT 'EUR',
            duration_minutes INT UNSIGNED NULL,
            target_price DECIMAL(12, 2) NULL,
            booking_url TEXT NULL,
            INDEX idx_route_date (origin, destination, departure_date),
            INDEX idx_searched_at (searched_at),
            INDEX idx_destination_price (destination, price)
        ) ENGINE=InnoDB;
        """
        with self.connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()

    def save_flight(self, flight: FlightData, target_price: float | None = None) -> int:
        """Insert one observed flight price and return its database ID."""
        query = """
        INSERT INTO flight_prices (
            searched_at, origin, destination, departure_date, return_date,
            airline, stops, price, currency, duration_minutes, target_price, booking_url
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        outbound = datetime.fromisoformat(flight.outbound_date).date()
        return_date = None
        if flight.return_date:
            return_date = datetime.fromisoformat(flight.return_date).date()

        values = (
            datetime.now(),
            flight.departure_airport_code,
            flight.destination_airport_code,
            outbound,
            return_date,
            flight.airline or None,
            flight.stop_overs,
            flight.price,
            "EUR",
            flight.duration_minutes,
            target_price,
            flight.booking_url or None,
        )
        with self.connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            row_id = cursor.lastrowid
            cursor.close()
        return int(row_id)
