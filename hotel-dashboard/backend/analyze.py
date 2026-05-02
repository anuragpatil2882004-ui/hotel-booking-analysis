import pandas as pd
import numpy as np
import json
import os

data = pd.read_csv("../data/bookings.csv")

# --- Summary Stats ---
total_bookings    = len(data)
total_canceled    = int(data["is_canceled"].sum())
cancellation_rate = round(total_canceled / total_bookings * 100, 2)
total_revenue     = int(data[data["is_canceled"] == 0]["total_cost"].sum())
avg_lead_time     = round(data["lead_time"].mean(), 2)

# --- Cancellations by hotel type ---
cancel_by_type = (
    data.groupby("hotel_type")["is_canceled"]
    .agg(["sum", "count"])
    .rename(columns={"sum": "canceled", "count": "total"})
    .reset_index()
)
cancel_by_type["rate"] = round(cancel_by_type["canceled"] / cancel_by_type["total"] * 100, 2)

# --- Lead time buckets ---
bins   = [0, 20, 40, 60, 80, 100]
labels = ["0-20", "21-40", "41-60", "61-80", "81-100"]
data["lead_bucket"] = pd.cut(data["lead_time"], bins=bins, labels=labels)
lead_cancel = (
    data.groupby("lead_bucket", observed=True)["is_canceled"]
    .mean().mul(100).round(2).reset_index()
)

# --- Revenue by hotel type ---
revenue_by_type = (
    data[data["is_canceled"] == 0]
    .groupby("hotel_type")["total_cost"]
    .sum().reset_index()
)

# --- Stay duration vs cancellation ---
stay_cancel = (
    data.groupby("stay_duration")["is_canceled"]
    .mean().mul(100).round(2).reset_index()
)

# --- Cancellation by star rating ---
cancel_by_star = (
    data.groupby("star_rating")["is_canceled"]
    .mean().mul(100).round(2).reset_index()
    .rename(columns={"is_canceled": "rate"})
)
star_order = {"normal": 0, "3": 1, "4": 2, "5": 3}
cancel_by_star["order"] = cancel_by_star["star_rating"].map(star_order)
cancel_by_star = cancel_by_star.sort_values("order").drop("order", axis=1)

# --- Cancellation by demand area ---
cancel_by_demand = (
    data.groupby("demand")["is_canceled"]
    .mean().mul(100).round(2).reset_index()
    .rename(columns={"is_canceled": "rate"})
)
demand_order = {"Very High": 0, "High": 1, "Medium": 2, "Low": 3}
cancel_by_demand["order"] = cancel_by_demand["demand"].map(demand_order)
cancel_by_demand = cancel_by_demand.sort_values("order").drop("order", axis=1)

# --- Cancellation by AC type ---
cancel_by_ac = (
    data.groupby("ac_type")["is_canceled"]
    .mean().mul(100).round(2).reset_index()
    .rename(columns={"is_canceled": "rate"})
)

summary = {
    "total_bookings":   total_bookings,
    "total_canceled":   total_canceled,
    "cancellation_rate": cancellation_rate,
    "total_revenue":    total_revenue,
    "avg_lead_time":    avg_lead_time,
    "cancel_by_type":   cancel_by_type.to_dict(orient="records"),
    "lead_cancel":      lead_cancel.to_dict(orient="records"),
    "revenue_by_type":  revenue_by_type.to_dict(orient="records"),
    "stay_cancel":      stay_cancel.to_dict(orient="records"),
    "cancel_by_star":   cancel_by_star.to_dict(orient="records"),
    "cancel_by_demand": cancel_by_demand.to_dict(orient="records"),
    "cancel_by_ac":     cancel_by_ac.to_dict(orient="records"),
}

os.makedirs("../data", exist_ok=True)
with open("../data/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Analysis complete: ../data/summary.json")
print(f"Total: {total_bookings:,} | Canceled: {total_canceled:,} | Rate: {cancellation_rate}%")
