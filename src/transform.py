
from pathlib import Path

import pandas as pd


# 1. Define project and file paths
PROJECT_DIR = Path(__file__).resolve().parents[1]

FILE_PATH = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "Ecommerce_Data_Engineering_Challenge.xlsx"
)

PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
CLEAN_FILE_PATH = PROCESSED_DIR / "clean_orders.csv"
QUARANTINE_PATH = PROJECT_DIR / "data" / "quarantine_orders.csv"


def main():
    # 2. Check whether the source file exists
    if not FILE_PATH.exists():
        raise FileNotFoundError(
            f"Source Excel file not found: {FILE_PATH}"
        )

    # 3. Load orders and product reference data
    data = pd.read_excel(FILE_PATH)
    products = pd.read_excel(FILE_PATH, sheet_name="Products")

    print("\nOriginal region counts:")
    print(data["region"].value_counts(dropna=False))
    print("Original rows:", len(data))

    # 4. Remove duplicate rows
    clean_data = data.drop_duplicates().copy()
    print("Rows after removing duplicates:", len(clean_data))

    # 5. Create a quarantine list
    quarantine_list = []

    def quarantine_rows(rows, reason):
        if not rows.empty:
            records = rows[["order_id"]].copy()
            records["quarantine_reason"] = reason
            quarantine_list.append(records)

    # 6. Handle missing customer IDs
    bad_rows = clean_data[clean_data["customer_id"].isna()]
    quarantine_rows(bad_rows, "Missing customer ID")
    clean_data = clean_data.dropna(subset=["customer_id"]).copy()

    # 7. Handle missing product IDs
    bad_rows = clean_data[clean_data["product_id"].isna()]
    quarantine_rows(bad_rows, "Missing product ID")
    clean_data = clean_data.dropna(subset=["product_id"]).copy()

    # 8. Fill missing prices using product reference prices
    price_lookup = products[["product_id", "standard_price"]]

    clean_data = clean_data.merge(
        price_lookup,
        on="product_id",
        how="left",
        validate="many_to_one",
    )

    clean_data["unit_price"] = clean_data["unit_price"].fillna(
        clean_data["standard_price"]
    )

    clean_data = clean_data.drop(columns=["standard_price"])

    # Quarantine prices that remain missing
    bad_rows = clean_data[clean_data["unit_price"].isna()]
    quarantine_rows(bad_rows, "Missing unit price after lookup")
    clean_data = clean_data.dropna(subset=["unit_price"]).copy()

    # 9. Handle missing regions
    bad_rows = clean_data[clean_data["region"].isna()]
    quarantine_rows(bad_rows, "Missing region")
    clean_data = clean_data.dropna(subset=["region"]).copy()

    # Standardise region names
    clean_data["region"] = (
        clean_data["region"].str.strip().str.title()
    )

    print("\nRegion counts after standardisation:")
    print(clean_data["region"].value_counts(dropna=False))

    # 10. Remove invalid quantities
    bad_rows = clean_data[clean_data["quantity"] <= 0]
    quarantine_rows(bad_rows, "Invalid quantity")
    clean_data = clean_data[clean_data["quantity"] > 0].copy()

    # 11. Remove invalid discounts
    bad_rows = clean_data[
        (clean_data["discount_pct"] < 0)
        | (clean_data["discount_pct"] > 1)
    ]
    quarantine_rows(bad_rows, "Invalid discount")

    clean_data = clean_data[
        (clean_data["discount_pct"] >= 0)
        & (clean_data["discount_pct"] <= 1)
    ].copy()

    # 12. Create output folders
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    QUARANTINE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # 13. Save clean data
    clean_data.to_csv(CLEAN_FILE_PATH, index=False)

    # 14. Save quarantine data
    if quarantine_list:
        quarantine_data = pd.concat(
            quarantine_list,
            ignore_index=True,
        )
    else:
        quarantine_data = pd.DataFrame(
            columns=["order_id", "quarantine_reason"]
        )

    quarantine_data.to_csv(QUARANTINE_PATH, index=False)

    # 15. Display final results
    print("\nTRANSFORMATION SUMMARY")
    print("----------------------")
    print("Clean rows:", len(clean_data))
    print("Quarantine records:", len(quarantine_data))

    print("\nQuarantine reasons:")
    print(quarantine_data["quarantine_reason"].value_counts())

    print("\nMissing values:", clean_data.isna().sum().sum())
    print("Duplicate rows:", clean_data.duplicated().sum())
    print(
        "Invalid quantities:",
        (clean_data["quantity"] <= 0).sum(),
    )
    print(
        "Invalid discounts:",
        (
            (clean_data["discount_pct"] < 0)
            | (clean_data["discount_pct"] > 1)
        ).sum(),
    )
    print(
        "Missing unit prices:",
        clean_data["unit_price"].isna().sum(),
    )

    print("\nClean file saved:", CLEAN_FILE_PATH)
    print("Quarantine file saved:", QUARANTINE_PATH)


if __name__ == "__main__":
    main()
