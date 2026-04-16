import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

st.title("📊 Retail Analytics Dashboard")
st.markdown("### Real-time Business Insights for Retail Decision Making")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("outputs/inventory_optimized.csv")
    df.columns = df.columns.str.lower()
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔎 Filters")

# Filter by Store
if "store_id" in df.columns:
    store = st.sidebar.selectbox("Select Store", sorted(df["store_id"].unique()))
    df = df[df["store_id"] == store]

# Filter by Item
if "item_id" in df.columns:
    item = st.sidebar.selectbox("Select Item", sorted(df["item_id"].unique()))
    df = df[df["item_id"] == item]

# -----------------------------
# KPI METRICS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

total_sales = df["qty_sold"].sum() if "qty_sold" in df.columns else 0
avg_sales = df["qty_sold"].mean() if "qty_sold" in df.columns else 0
current_stock = df["stock_on_hand"].iloc[-1] if "stock_on_hand" in df.columns else 0
order_qty = df["order_quantity"].iloc[-1] if "order_quantity" in df.columns else 0

col1.metric("📦 Total Sales", int(total_sales))
col2.metric("📈 Avg Sales", round(avg_sales, 2))
col3.metric("🏬 Current Stock", int(current_stock))
col4.metric("🛒 Suggested Order", int(order_qty))

# -----------------------------
# SALES TREND
# -----------------------------
st.subheader("📈 Sales Trend")

if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    st.line_chart(df.set_index("date")["qty_sold"])

# -----------------------------
# INVENTORY VS DEMAND
# -----------------------------
st.subheader("📊 Inventory vs Demand")

if "stock_on_hand" in df.columns and "qty_sold" in df.columns:
    chart_df = df[["qty_sold", "stock_on_hand"]]
    st.bar_chart(chart_df)

# -----------------------------
# EOQ & ORDER ANALYSIS
# -----------------------------
st.subheader("📦 Order Optimization")

if "eoq" in df.columns and "order_quantity" in df.columns:
    st.write("EOQ vs Final Order Quantity")
    st.bar_chart(df[["eoq", "order_quantity"]])

# -----------------------------
# LOW STOCK ALERT 🚨
# -----------------------------
st.subheader("🚨 Inventory Alerts")

if "stock_on_hand" in df.columns and "qty_sold" in df.columns:
    latest_stock = df["stock_on_hand"].iloc[-1]
    avg_demand = df["qty_sold"].mean()

    if latest_stock < avg_demand:
        st.error("⚠️ Low Stock Alert! Consider reordering immediately.")
    else:
        st.success("✅ Stock level is sufficient.")

# -----------------------------
# DATA TABLE
# -----------------------------
st.subheader("📋 Data Preview")
st.dataframe(df.tail(20))