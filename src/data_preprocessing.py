import pandas as pd

def load_and_clean_data(path):

    df = pd.read_csv(path, parse_dates=["date"])

    print("\n🔍 Initial Shape:", df.shape)

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df = df.dropna()

    # Remove negative sales (if any)
    df = df[df["qty_sold"] >= 0]

    # Handle stockouts (important)
    if "stockout_flag" in df.columns:
        df = df[df["stockout_flag"] == 0]

    print("✅ Cleaned Shape:", df.shape)

    return df


if __name__ == "__main__":

    df = load_and_clean_data("data/raw/retail_data.csv")

    df.to_csv("data/processed/cleaned_data.csv", index=False)

    print("\n✅ Data Preprocessing Completed!")