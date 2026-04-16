import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error


def train_model(df):

    # =========================
    # FEATURES & TARGET
    # =========================
    features = [
        "lag_1", "lag_7", "lag_14",
        "rolling_mean_7", "rolling_mean_14",
        "rolling_std_7",
        "day_of_week", "month",
        "price", "discount_pct", "on_promo"
    ]

    target = "qty_sold"

    X = df[features]
    y = df[target]

    # =========================
    # TRAIN TEST SPLIT
    # =========================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # =========================
    # MODEL
    # =========================
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # =========================
    # PREDICTIONS
    # =========================
    y_pred = model.predict(X_test)

    # =========================
    # METRICS
    # =========================
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5

    print("\n📊 MODEL PERFORMANCE")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")

    # =========================
    # SAVE MODEL
    # =========================
    os.makedirs("models", exist_ok=True)

    joblib.dump(model, "models/forecast_model.pkl")

    return model, X_test, y_test, y_pred


if __name__ == "__main__":

    df = pd.read_csv("data/processed/featured_data.csv")

    model, X_test, y_test, y_pred = train_model(df)

    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(y_test.values[:100], label="Actual")
    plt.plot(y_pred[:100], label="Predicted")
    plt.legend()
    plt.title("Actual vs Predicted Sales")
    plt.savefig("images/10_actual_vs_pred.png")
    plt.close()

    print("\n✅ Model Training Completed!")
    print("📁 Model saved in models/forecast_model.pkl")

