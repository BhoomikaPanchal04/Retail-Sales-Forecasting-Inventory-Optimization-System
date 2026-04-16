import pandas as pd
import matplotlib.pyplot as plt
import os

# Create images folder if not exists
os.makedirs("images", exist_ok=True)

# =========================
# 1. LOAD DATA
# =========================
df = pd.read_csv("data/raw/retail_data.csv", parse_dates=["date"])

print("\n✅ DATA LOADED")
print(df.head())

# Save preview
df.head().to_csv("images/01_dataset_preview.csv", index=False)

# =========================
# 2. BASIC INFO
# =========================
print("\n🔍 DATA INFO")
print(df.info())

print("\n🔍 DESCRIPTION")
print(df.describe())

# =========================
# 3. TOTAL SALES TREND
# =========================
daily_sales = df.groupby("date")["qty_sold"].sum()

plt.figure()
daily_sales.plot()
plt.title("Total Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.savefig("images/03_sales_trend.png")
plt.close()

# =========================
# 4. DAY OF WEEK ANALYSIS
# =========================
df["day_of_week"] = df["date"].dt.day_name()

dow_sales = df.groupby("day_of_week")["qty_sold"].mean()

dow_sales = dow_sales.reindex([
    "Monday","Tuesday","Wednesday","Thursday",
    "Friday","Saturday","Sunday"
])

plt.figure()
dow_sales.plot(kind="bar")
plt.title("Average Sales by Day of Week")
plt.savefig("images/04_weekday_sales.png")
plt.close()

# =========================
# 5. PROMOTION IMPACT
# =========================
promo_sales = df.groupby("on_promo")["qty_sold"].mean()

plt.figure()
promo_sales.plot(kind="bar")
plt.title("Sales with vs without Promotion")
plt.xticks([0,1], ["No Promo", "Promo"], rotation=0)
plt.savefig("images/05_promo_impact.png")
plt.close()

# =========================
# 6. PRODUCT ANALYSIS
# =========================
top_products = df.groupby("item_id")["qty_sold"].sum().sort_values(ascending=False)

plt.figure()
top_products.head(10).plot(kind="bar")
plt.title("Top Selling Products")
plt.savefig("images/06_top_products.png")
plt.close()

# =========================
# 7. INTERMITTENT DEMAND
# =========================
zero_demand = df.groupby("item_id")["qty_sold"].apply(lambda x: (x==0).mean())

print("\n📊 ZERO DEMAND RATIO (INTERMITTENT DEMAND):")
print(zero_demand)

zero_demand.to_csv("images/08_zero_demand.csv")

# =========================
# 8. STORE ANALYSIS
# =========================
store_sales = df.groupby("store_id")["qty_sold"].sum()

plt.figure()
store_sales.plot(kind="bar")
plt.title("Sales by Store")
plt.savefig("images/07_store_sales.png")
plt.close()

# =========================
# FINAL MESSAGE
# =========================
print("\n✅ EDA COMPLETED SUCCESSFULLY!")
print("📁 Check 'images/' folder for outputs.")