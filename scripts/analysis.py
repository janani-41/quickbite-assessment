import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "cleaned_data" / "Quick_Bite_Combined_Data.xlsx"
OUTPUT_DIR = BASE_DIR / "analysis"
def load_data():
    return pd.read_excel(INPUT_FILE)
def filter_delivered(df):
    return df[
        df["order_status"].str.lower() == "delivered"
    ].copy()
def area_performance(df):
    result = df.groupby(
        ["area_name", "city"]
    ).agg(
        total_orders=("order_id", "nunique"),
        revenue=("order_amount", "sum"),
        average_order_value=("order_amount", "mean"),
        average_delivery_time=("delivery_minutes", "mean"),
        late_deliveries=("is_late", "sum"),
        average_rating=("rating", "mean")
    ).reset_index()
    result["late_delivery_rate"] = (
        result["late_deliveries"] /
        df.groupby(["area_name", "city"])["delivery_minutes"].count().values
    ) * 100
    result = result.sort_values(
        "revenue", ascending=False
    )
    result.insert(
        0, "rank",
        result["revenue"].rank(
            method="dense", ascending=False
        ).astype(int)
    )
    return result.round(2)
def top_cuisine_by_day(df):
    result = df.groupby(
        ["order_day", "cuisine"]
    ).size().reset_index(name="cuisine_orders")
    result["total_day_orders"] = (
        result.groupby("order_day")["cuisine_orders"]
        .transform("sum")
    )
    result["order_share"] = (
        result["cuisine_orders"] /
        result["total_day_orders"] * 100
    )
    result = result[
        result["cuisine_orders"] ==
        result.groupby("order_day")["cuisine_orders"].transform("max")
    ]
    days = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]
    result["order_day"] = pd.Categorical(
        result["order_day"],
        categories=days,
        ordered=True
    )
    return result.sort_values("order_day").round(2)
def vehicle_performance(df):
    result = df.groupby(
        "vehicle_type"
    ).agg(
        total_orders=("order_id", "nunique"),
        average_delivery_time=("delivery_minutes", "mean"),
        late_deliveries=("is_late", "sum"),
        average_rating=("rating", "mean")
    ).reset_index()
    result["late_delivery_rate"] = (
        result["late_deliveries"] /
        df.groupby("vehicle_type")["delivery_minutes"].count().values
    ) * 100
    return result.sort_values(
        "average_delivery_time"
    ).round(2)
def main():
    df = load_data()
    delivered = filter_delivered(df)
    area = area_performance(delivered)
    cuisine = top_cuisine_by_day(delivered)
    vehicle = vehicle_performance(delivered)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(
        OUTPUT_DIR / "Quick_Bite_Analysis.xlsx"
    ) as writer:
        area.to_excel(
            writer,
            sheet_name="Area Performance",
            index=False
        )
        cuisine.to_excel(
            writer,
            sheet_name="Top Cuisine by Day",
            index=False
        )
        vehicle.to_excel(
            writer,
            sheet_name="Vehicle Performance",
            index=False
        )
    print("Analysis completed successfully!")
if __name__ == "__main__":
    main()
