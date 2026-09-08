"""Streamlit dashboard for historical flight-price analytics."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from analytics import FlightAnalytics
from database import FlightDatabase, DatabaseError


st.set_page_config(page_title="Flight Price Analytics", page_icon="✈️", layout="wide")
st.title("✈️ Flight Price Analytics")
st.caption("Historical fare intelligence powered by MySQL, Python, Streamlit and Plotly")


def money(value: float | None) -> str:
    return "—" if value is None else f"€{value:,.2f}"


try:
    database = FlightDatabase()
    analytics = FlightAnalytics(database)
    routes = analytics.routes()
except (DatabaseError, ValueError) as error:
    st.error(f"Could not connect to MySQL: {error}")
    st.info("Configure MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD and MYSQL_DATABASE in .env.")
    st.stop()

if not routes:
    st.warning("No historical price observations are available yet. Run `python main.py` to collect data.")
    st.stop()

route_labels = [f"{row['origin']} → {row['destination']}" for row in routes]
selected_route = st.sidebar.selectbox("Route", route_labels)
origin, destination = selected_route.split(" → ", 1)

lowest = analytics.lowest_price(origin, destination)
average = analytics.average_price(origin, destination)
latest = analytics.latest_price(origin, destination)
comparison = analytics.target_vs_actual(origin, destination)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Current Price", money(latest))
col2.metric("Lowest Price", money(lowest))
col3.metric("Average Price", money(average))

variance = comparison["variance"]
col4.metric("Target Variance", money(variance), delta=None if variance is None else f"{variance:+.2f}")

st.subheader(f"Price Trend — {origin} → {destination}")
trend = analytics.price_trend(origin, destination)
if trend:
    frame = pd.DataFrame(trend)
    frame["searched_at"] = pd.to_datetime(frame["searched_at"])
    chart = px.line(frame, x="searched_at", y="price", markers=True, hover_data=["airline", "stops", "departure_date"])
    chart.update_layout(xaxis_title="Search Time", yaxis_title="Price (EUR)")
    st.plotly_chart(chart, use_container_width=True)
else:
    st.info("Not enough historical observations for a trend chart.")

st.subheader("Target vs Actual")
target_col, actual_col = st.columns(2)
target_col.metric("Target", money(comparison["target"]))
actual_col.metric("Actual", money(comparison["actual"]))

st.subheader(f"Cheapest Destinations from {origin}")
cheapest = analytics.cheapest_destinations(origin)
if cheapest:
    destination_frame = pd.DataFrame(cheapest)
    destination_frame.columns = ["Destination", "Lowest Price", "Average Price"]
    st.dataframe(destination_frame, use_container_width=True, hide_index=True)
else:
    st.info("No destination history is available yet.")
