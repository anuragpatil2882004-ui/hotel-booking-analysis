import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 50000

# --- Location pool with demand tiers ---
city_locations = [
    ("Mumbai", "Very High"), ("Delhi", "Very High"), ("Bengaluru", "Very High"),
    ("Hyderabad", "High"), ("Chennai", "High"), ("Kolkata", "High"), ("Pune", "High"),
    ("Ahmedabad", "Medium"), ("Jaipur", "Medium"), ("Surat", "Medium"),
    ("Lucknow", "Medium"), ("Chandigarh", "Medium"), ("Kochi", "Medium"),
    ("Indore", "Low"), ("Bhopal", "Low"),
]
resort_locations = [
    ("Goa", "Very High"), ("Shimla", "Very High"), ("Manali", "Very High"), ("Udaipur", "Very High"),
    ("Ooty", "High"), ("Munnar", "High"), ("Coorg", "High"),
    ("Rishikesh", "High"), ("Darjeeling", "High"), ("Andaman Islands", "High"),
    ("Mussoorie", "Medium"), ("Kasauli", "Medium"), ("Lonavala", "Medium"), ("Mahabaleshwar", "Medium"),
    ("Kodaikanal", "Low"),
]

# Demand → weight for sampling (higher demand = more bookings)
demand_weight = {"Very High": 4, "High": 3, "Medium": 2, "Low": 1}

def weighted_sample(pool, size):
    weights = np.array([demand_weight[d] for _, d in pool], dtype=float)
    weights /= weights.sum()
    idx = np.random.choice(len(pool), size=size, p=weights)
    return [pool[i] for i in idx]

# --- Base price matrix [Very High, High, Medium, Low] ---
base_price = {
    ("normal", "ac"):    [1800, 1200,  800,  500],
    ("normal", "nonac"): [1200,  800,  500,  350],
    ("3",      "ac"):    [3500, 2800, 2000, 1400],
    ("3",      "nonac"): [2500, 2000, 1400,  900],
    ("4",      "ac"):    [7000, 5500, 4000, 2800],
    ("4",      "nonac"): [5000, 4000, 2800, 2000],
    ("5",      "ac"):    [15000,11000,8000, 5500],
    ("5",      "nonac"): [11000,8000, 5500, 4000],
}
demand_idx = {"Very High": 0, "High": 1, "Medium": 2, "Low": 3}

# --- Generate base columns ---
hotel_type   = np.random.choice(["City", "Resort"], n, p=[0.55, 0.45])
star_rating  = np.random.choice(["normal", "3", "4", "5"], n, p=[0.25, 0.35, 0.25, 0.15])
ac_type      = np.random.choice(["ac", "nonac"], n, p=[0.65, 0.35])
lead_time    = np.random.randint(1, 100, n)
stay_duration = np.random.randint(1, 10, n)

city_samples   = weighted_sample(city_locations,   n)
resort_samples = weighted_sample(resort_locations, n)

locations, demands = [], []
for i in range(n):
    loc, dem = city_samples[i] if hotel_type[i] == "City" else resort_samples[i]
    locations.append(loc)
    demands.append(dem)

# --- Realistic price with ±30% noise around market rate ---
prices = []
for i in range(n):
    key = (star_rating[i], ac_type[i])
    market = base_price[key][demand_idx[demands[i]]]
    noise  = np.random.uniform(0.7, 1.3)
    prices.append(int(market * noise))

# --- Cancellation probability driven by real factors ---
cancel_probs = []
for i in range(n):
    p = 0.15  # base

    # Lead time
    lt = lead_time[i]
    if   41 <= lt <= 60: p += 0.12
    elif 21 <= lt <= 40: p += 0.08
    elif 61 <= lt <= 80: p += 0.04

    # Stay duration
    sd = stay_duration[i]
    if   sd == 7:  p += 0.10
    elif sd <= 4:  p += 0.06

    # Hotel type
    if hotel_type[i] == "City": p += 0.03

    # Star
    star_add = {"normal": 0, "3": 0.03, "4": 0.07, "5": 0.12}
    p += star_add[star_rating[i]]

    # AC
    if ac_type[i] == "ac": p += 0.03

    # Price vs market — penalty heavier in low demand
    key    = (star_rating[i], ac_type[i])
    market = base_price[key][demand_idx[demands[i]]]
    ratio  = prices[i] / market
    dm     = {"Very High": 0.5, "High": 0.75, "Medium": 1.0, "Low": 1.75}[demands[i]]
    if   ratio > 1.5: p += 0.15 * dm
    elif ratio > 1.2: p += 0.10 * dm
    elif ratio > 1.0: p += 0.04 * dm
    elif ratio < 0.6: p += 0.05  # too cheap = low commitment

    # Demand area
    demand_add = {"Very High": 0.04, "High": 0.02, "Medium": 0.0, "Low": -0.03}
    p += demand_add[demands[i]]

    cancel_probs.append(min(max(p, 0.05), 0.95))

is_canceled = np.array([np.random.choice([0, 1], p=[1 - cp, cp]) for cp in cancel_probs])

data = pd.DataFrame({
    "booking_id":    range(1, n + 1),
    "hotel_type":    hotel_type,
    "location":      locations,
    "demand":        demands,
    "star_rating":   star_rating,
    "ac_type":       ac_type,
    "lead_time":     lead_time,
    "stay_duration": stay_duration,
    "price_per_night": prices,
    "total_cost":    np.array(prices) * stay_duration,
    "is_canceled":   is_canceled,
})

os.makedirs("../data", exist_ok=True)
data.to_csv("../data/bookings.csv", index=False)
print(f"Generated {n} records → ../data/bookings.csv")
print(data.head())
print(f"\nCancellation rate: {data['is_canceled'].mean()*100:.1f}%")
