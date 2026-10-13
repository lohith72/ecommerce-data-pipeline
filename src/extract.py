
from pathlib import Path

import pandas as pd


# 1. Locate the project and source Excel file
PROJECT_DIR = Path(__file__).resolve().parents[1]

file_path = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "Ecommerce_Data_Engineering_Challenge.xlsx"
)


def main():
    # 2. Check whether the source file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"Source Excel file not found: {file_path}"
        )

    # 3. Extract orders and product reference data
    data = pd.read_excel(file_path)
    products = pd.read_excel(file_path, sheet_name="Products")

    print("E-COMMERCE DATA QUALITY REPORT")
    print("-" * 35)

    # 4. Dataset overview
    print("\nDataset overview:")
    print("Total orders:", len(data))
    print("Columns:", data.columns.tolist())

    # 5. Check missing values
    print("\nMissing values:")
    print(data.isnull().sum())

    # 6. Check duplicate records
    print("\nDuplicate rows:", data.duplicated().sum())

    # 7. Check invalid quantities
    print("\nInvalid quantities:")
    print(data[data["quantity"] <= 0])

    # 8. Check invalid discounts
    print("\nInvalid discounts:")
    print(
        data[
            (data["discount_pct"] < 0)
            | (data["discount_pct"] > 1)
        ]
    )

    # 9. Check region values
    print("\nRegion values:")
    print(data["region"].value_counts(dropna=False))

    # 10. Check missing IDs and prices
    print(
        "\nMissing customer IDs:",
        data["customer_id"].isnull().sum()
    )
    print(
        "Missing product IDs:",
        data["product_id"].isnull().sum()
    )
    print(
        "Missing unit prices:",
        data["unit_price"].isnull().sum()
    )

    # 11. Check product reference prices
    print("\nProducts with IDs P0044 and P0173:")
    print(
        products[
            products["product_id"].isin(["P0044", "P0173"])
        ]
    )

    print("\nData inspection completed.")


if __name__ == "__main__":
    main()
