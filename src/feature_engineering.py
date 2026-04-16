import pandas as pd
import os

def create_features(df):

    # Sort properly
    df = df.sort_values(["store_id", "item_id", "date"])

    # =========================
    # LAG FEATURES
    # =========================
    df["lag_1"] = df.groupby(["store_id", "item_id"])["qty_sold"].shift(1)
    df["lag_7"] = df.groupby(["store_id", "item_id"])["qty_sold"].shift(7)
    df["lag_14"] = df.groupby(["store_id", "item_id"])["qty_sold"].shift(14)

    # =========================
    # ROLLING FEATURES
    # =========================
    df["rolling_mean_7"] = df.groupby(["store_id", "item_id"])["qty_sold"].shift(1).rolling(7).mean()
    df["rolling_mean_14"] = df.groupby(["store_id", "item_id"])["qty_sold"].shift(1).rolling(14).mean()

    df["rolling_std_7"] = df.groupby(["store_id", "item_id"])["qty_sold"].shift(1).rolling(7).std()

    # =========================
    # TIME FEATURES
    # =========================
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month

    # =========================
    # DROP NULLS (VERY IMPORTANT)
    # =========================
    df = df.dropna()

    return df


if __name__ == "__main__":

    os.makedirs("data/processed", exist_ok=True)

    df = pd.read_csv("data/processed/cleaned_data.csv", parse_dates=["date"])
    df = create_features(df)

    df.to_csv("data/processed/featured_data.csv", index=False)

    print("✅ Feature Engineering Completed!")
    print("📁 Saved to data/processed/featured_data.csv")