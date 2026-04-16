import pandas as pd
import numpy as np
import os


def optimize_inventory(latest_data):
    """
    Inventory Optimization with EOQ
    """

    # 🔹 Standardize column names
    latest_data.columns = latest_data.columns.str.lower()

    # 🔹 Constants
    ordering_cost = 50

    # 🔹 Create holding cost from rate if needed
    if "holding_cost" not in latest_data.columns:
        if "holding_cost_rate" in latest_data.columns and "unit_cost" in latest_data.columns:
            latest_data["holding_cost"] = latest_data["holding_cost_rate"] * latest_data["unit_cost"]
        else:
            latest_data["holding_cost"] = 5  # fallback

    # 🔹 ✅ FIXED: Use qty_sold as demand
    if "annual_demand" not in latest_data.columns:
        latest_data["annual_demand"] = latest_data["qty_sold"] * 12

    # 🔹 EOQ Calculation
    latest_data["eoq"] = (
        (2 * latest_data["annual_demand"] * ordering_cost)
        / latest_data["holding_cost"]
    ) ** 0.5

    # 🔹 Use stock_on_hand instead of stock
    if "stock_on_hand" in latest_data.columns:
        latest_data["order_quantity"] = latest_data["annual_demand"] - latest_data["stock_on_hand"]
    else:
        latest_data["order_quantity"] = latest_data["annual_demand"]

    # 🔹 Final Order Quantity
    latest_data["order_quantity"] = latest_data[["order_quantity", "eoq"]].max(axis=1)

    # 🔹 Avoid negative values
    latest_data["order_quantity"] = latest_data["order_quantity"].apply(
        lambda x: max(0, int(x))
    )

    return latest_data


# 🚀 Run file
if __name__ == "__main__":

    print("📦 Running Inventory Optimization...")

    os.makedirs("outputs", exist_ok=True)

    df = pd.read_csv("data/processed/featured_data.csv")

    print("✅ Data Loaded:", df.shape)
    print("📊 Columns:", df.columns.tolist())

    optimized_df = optimize_inventory(df)

    output_path = "outputs/inventory_optimized.csv"
    optimized_df.to_csv(output_path, index=False)

    print("✅ Optimization Completed!")
    print(f"📁 Saved at: {output_path}")