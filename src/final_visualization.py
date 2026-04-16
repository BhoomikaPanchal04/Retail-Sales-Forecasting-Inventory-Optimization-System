import pandas as pd
import matplotlib.pyplot as plt
import os

# Create images folder
os.makedirs("images", exist_ok=True)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/processed/featured_data.csv")
inventory = pd.read_csv("outputs/inventory_recommendations.csv")

print("✅ Data Loaded")

# =========================
# 1. FORECAST VS ACTUAL (SIMULATED)
# =========================
sample = df.tail(100)

plt.figure()
plt.plot(sample["qty_sold"].values, label="Actual")
plt.plot(sample["rolling_mean_7"].values, label="Predicted (Proxy)")
plt.legend()
plt.title("Sales Forecast vs Actual")
plt.savefig("images/12_forecast_vs_actual.png")
plt.close()

# =========================
# 2. INVENTORY DISTRIBUTION
# =========================
plt.figure()
inventory["order_quantity"].hist()
plt.title("Distribution of Order Quantity")
plt.savefig("images/13_order_distribution.png")
plt.close()

# =========================
# 3. TOP REORDER PRODUCTS
# =========================
top_reorder = inventory.sort_values("order_quantity", ascending=False).head(10)

plt.figure()
plt.bar(top_reorder["item_id"], top_reorder["order_quantity"])
plt.title("Top Products to Reorder")
plt.savefig("images/14_top_reorder.png")
plt.close()

# =========================
# 4. STOCK ALERTS
# =========================
alerts = inventory[inventory["order_quantity"] > 0]

alerts.to_csv("outputs/reorder_alerts.csv", index=False)

print("\n🚨 REORDER ALERTS GENERATED")
print(alerts[["store_id", "item_id", "order_quantity"]].head())

# =========================
# 5. BUSINESS SUMMARY
# =========================
total_orders = inventory["order_quantity"].sum()
products_to_reorder = len(alerts)

print("\n📊 BUSINESS SUMMARY")
print(f"Total Order Quantity: {total_orders}")
print(f"Products to Reorder: {products_to_reorder}")

print("\n✅ Visualization Completed!")
print("📁 Check 'images/' and 'outputs/' folders")