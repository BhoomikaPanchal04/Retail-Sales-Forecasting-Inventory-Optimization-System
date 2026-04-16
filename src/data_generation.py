import pandas as pd
import numpy as np

def generate_retail_data():

    np.random.seed(42)

    # Config
    num_days = 365
    num_stores = 3
    num_products = 10

    dates = pd.date_range(start="2023-01-01", periods=num_days)

    data = []

    for store in range(1, num_stores + 1):
        for product in range(1, num_products + 1):

            base_demand = np.random.randint(20, 50)

            for date in dates:

                # Seasonality (weekly pattern)
                day_of_week = date.dayofweek
                seasonal_factor = 1.2 if day_of_week in [5, 6] else 1.0

                # Random noise
                noise = np.random.normal(0, 5)

                # Promotion
                on_promo = np.random.choice([0, 1], p=[0.8, 0.2])
                discount = np.random.randint(10, 30) if on_promo else 0

                promo_boost = 1.5 if on_promo else 1.0

                # Final demand
                qty_sold = max(0, int(base_demand * seasonal_factor * promo_boost + noise))

                # Stockout simulation
                stock_on_hand = np.random.randint(20, 100)
                stockout_flag = 1 if qty_sold > stock_on_hand else 0

                # Price
                price = np.random.randint(50, 200)

                data.append([
                    date,
                    f"S{store}",
                    f"P{product}",
                    qty_sold,
                    price,
                    discount,
                    on_promo,
                    stockout_flag,
                    stock_on_hand,
                    7,   # lead time
                    100, # unit cost
                    0.2  # holding cost
                ])

    df = pd.DataFrame(data, columns=[
        "date", "store_id", "item_id", "qty_sold",
        "price", "discount_pct", "on_promo",
        "stockout_flag", "stock_on_hand",
        "lead_time_days", "unit_cost", "holding_cost_rate"
    ])

    return df


import os

if __name__ == "__main__":
    df = generate_retail_data()

    # Create directory if not exists
    os.makedirs("data/raw", exist_ok=True)

    df.to_csv("data/raw/retail_data.csv", index=False)

    print("Dataset generated successfully!")