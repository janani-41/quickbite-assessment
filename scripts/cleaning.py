import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "QuickBite_Assessment.xlsx"
OUTPUT_DIR = BASE_DIR / "cleaned_data"
def load_data():
    return pd.read_excel(INPUT_FILE, sheet_name=None)
def clean_data(tables):
    keys = {
        "areas": "area_id",
        "restaurants": "restaurant_id",
        "delivery_partners": "partner_id",
        "customers": "customer_id",
        "orders": "order_id",
        "feedback": "feedback_id"
    }
    for name, df in tables.items():
        df.columns = df.columns.str.strip()
        df = df.drop_duplicates()
        for col in df.select_dtypes("object").columns:
            df[col] = df[col].astype("string").str.strip()
        df = df.dropna(subset=[keys[name]])
        if name == "areas":
            city_map = {
                "BLR": "Bengaluru",
                "Hyd": "Hyderabad",
                "Madras": "Chennai",
                "MUMBAI": "Mumbai",
                "mumbai": "Mumbai",
                "chennai": "Chennai"
            }
            df["city"] = df["city"].replace(city_map)
            df["city"] = df["city"].str.title()
        if name == "restaurants":
            df["cuisine"] = df["cuisine"].str.lower().str.strip()
            cuisine_map = {
                "dessert": "Desserts",
                "biriyani": "Biryani",
                "n. indian": "North Indian",
                "north-indian": "North Indian",
                "south-indian": "South Indian",
                "italian - pizza": "Pizza"
            }
            df["cuisine"] = df["cuisine"].replace(cuisine_map).str.title()
        if name == "delivery_partners":
            df["vehicle_type"] = df["vehicle_type"].str.lower()
            vehicle_map = {
                "motor bike": "Motorbike",
                "bike": "Bike",
                "bicycle": "Bicycle",
                "activa": "Scooter",
                "scooty": "Scooter",
                "scooter": "Scooter",
                "ev scooter": "Electric Scooter",
                "e-scooter": "Electric Scooter"
            }
            df["vehicle_type"] = (
                df["vehicle_type"].replace(vehicle_map)
                .str.title()
            )
        if name == "orders":
            df["order_status"] = (
                df["order_status"].str.lower().str.strip()
            )
            df["order_status"] = df["order_status"].replace({
                "completed": "delivered",
                "canceled": "cancelled"
            }).str.title()
            df["payment_mode"] = (
                df["payment_mode"].str.lower().str.strip()
            )
            df["coupon_code"] = df["coupon_code"].str.upper()
            df["order_datetime"] = pd.to_datetime(
                df["order_datetime"],
                format="mixed",
                dayfirst=True,
                errors="coerce"
            )
            df["order_amount"] = pd.to_numeric(
                df["order_amount"], errors="coerce"
            )
            df["delivery_minutes"] = pd.to_numeric(
                df["delivery_minutes"].astype("string")
                .str.replace(" min", "", regex=False),
                errors="coerce"
            )
        if name == "feedback":
            df["rating"] = pd.to_numeric(
                df["rating"], errors="coerce"
            )
        df = df.drop_duplicates(
            subset=[keys[name]],
            keep="first"
        )
        tables[name] = df.reset_index(drop=True)
    return tables
def save_cleaned_data(tables):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(
        OUTPUT_DIR / "Quick_Bite_Data_Cleaning.xlsx"
    ) as writer:
        for name, df in tables.items():
            df.to_excel(writer, sheet_name=name, index=False)
def combine_data(tables):
    orders = tables["orders"]
    data = orders.merge(
        tables["customers"][["customer_id", "customer_name"]],
        on="customer_id", how="left"
    )
    data = data.merge(
        tables["restaurants"][
            ["restaurant_id", "restaurant_name", "area_id", "cuisine"]
        ],
        on="restaurant_id", how="left"
    )
    data = data.merge(
        tables["areas"][["area_id", "area_name", "city"]],
        on="area_id", how="left"
    )
    data = data.merge(
        tables["delivery_partners"][
            ["partner_id", "partner_name", "vehicle_type"]
        ],
        on="partner_id", how="left"
    )
    data = data.merge(
        tables["feedback"][["order_id", "rating", "comment"]],
        on="order_id", how="left"
    )
    data["order_date"] = data["order_datetime"].dt.date
    data["order_time"] = data["order_datetime"].dt.strftime("%H:%M")
    data["order_day"] = data["order_datetime"].dt.day_name()
    data["is_late"] = data["delivery_minutes"].gt(45).astype("boolean")
    columns = [
        "order_id", "order_date", "order_time", "order_day",
        "customer_name", "restaurant_name", "cuisine",
        "area_name", "city", "partner_name", "vehicle_type",
        "order_amount", "payment_mode", "coupon_code",
        "order_status", "delivery_minutes", "is_late",
        "rating", "comment"
    ]
    data = data[columns]
    assert data["order_id"].is_unique, "Duplicate orders found!"
    return data
def main():
    tables = load_data()
    tables = clean_data(tables)
    save_cleaned_data(tables)
    combined = combine_data(tables)
    combined.to_excel(
        OUTPUT_DIR / "Quick_Bite_Combined_Data.xlsx",
        index=False
    )
    print("Data cleaning and combining completed!")
if __name__ == "__main__":
    main()
