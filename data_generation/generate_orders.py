import pandas as pd
import random
import numpy as np
from faker import Faker
from pathlib import Path
from datetime import datetime

fake = Faker()

# -----------------------------
# Products
# -----------------------------
products = [
    ("Patio Chair", "Patio Furniture", 149.99),
    ("Outdoor Sofa", "Patio Furniture", 499.99),
    ("Garden Bench", "Patio Furniture", 249.99),
    ("Charcoal Grill", "BBQ & Grills", 299.99),
    ("Gas Grill", "BBQ & Grills", 599.99),
    ("Garden Hose", "Gardening", 39.99),
    ("Watering Can", "Gardening", 19.99),
    ("Outdoor Rug", "Outdoor Decor", 89.99),
    ("Lantern", "Outdoor Decor", 49.99),
    ("Storage Bin", "Home Storage", 29.99)
]

# -----------------------------
# Stores
# -----------------------------
stores = [
    "West Coast Online",
    "Texas Home Store",
    "Northeast Living",
    "Midwest Outdoors",
    "Southern Patio"
]

# -----------------------------
# Customers
# -----------------------------
customers = {}

for i in range(1, 2001):
    cid = f"CUST{i:04d}"

    customers[cid] = {
        "customer_name": fake.name(),
        "email": fake.email(),
        "state": random.choice([
            "California",
            "Texas",
            "Florida",
            "New York",
            "Illinois",
            "Georgia",
            "Arizona",
            "Washington"
        ])
    }

customer_ids = list(customers.keys())

# Creates realistic repeat customers
weights = np.random.pareto(1.5, len(customer_ids))

# -----------------------------
# Seasonality
# -----------------------------
month_weights = {
    1:0.6,
    2:0.7,
    3:1.0,
    4:1.3,
    5:1.6,
    6:1.8,
    7:1.7,
    8:1.4,
    9:1.1,
    10:0.9,
    11:1.2,
    12:1.4
}

rows = []

for i in range(5000):

    # repeat customers
    customer_id = random.choices(
        customer_ids,
        weights=weights,
        k=1
    )[0]

    customer = customers[customer_id]

    product_name, category, unit_price = random.choice(products)

    qty = random.randint(1, 4)

    revenue = round(qty * unit_price, 2)

    # date with seasonality
    while True:
        order_date = fake.date_between(
            start_date="-3y",
            end_date="today"
        )

        if random.random() < month_weights[order_date.month] / 2:
            break

    rows.append({
        "order_id": f"ORD{i:06d}",
        "order_date": order_date,
        "customer_id": customer_id,
        "customer_name": customer["customer_name"],
        "email": customer["email"],
        "state": customer["state"],
        "product_name": product_name,
        "category": category,
        "quantity": qty,
        "unit_price": unit_price,
        "revenue": revenue,
        "store_name": random.choice(stores)
    })

df = pd.DataFrame(rows)

# ----------------------------------
# Data Quality Issues
# ----------------------------------

# duplicate rows (2%)
df = pd.concat([
    df,
    df.sample(frac=0.02, random_state=42)
])

# missing order dates (1%)
df.loc[
    df.sample(frac=0.01, random_state=42).index,
    "order_date"
] = None

# negative revenue (0.5%)
neg_idx = df.sample(frac=0.005, random_state=42).index
df.loc[neg_idx, "revenue"] *= -1

# inconsistent product names
chair_idx = df[df["product_name"] == "Patio Chair"].sample(
    frac=0.2,
    random_state=42
).index

df.loc[chair_idx, "product_name"] = random.choice([
    "PATIO CHAIR",
    "patio-chair"
])

# ----------------------------------
# Save
# ----------------------------------

DATA_DIR = "/opt/airflow/data"

Path(DATA_DIR).mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    f"{DATA_DIR}/orders.csv",
    index=False
)

print(f"Generated {len(df)} records")