
import os
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv


# 1. Define project paths
PROJECT_DIR = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_DIR / "data" / "processed" / "clean_orders.csv"

# 2. Load credentials from the local .env file
load_dotenv(PROJECT_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "ecommerce_db"),
}

# 3. Validate required database settings
required_settings = ["user", "password"]

missing_settings = [
    setting
    for setting in required_settings
    if not DB_CONFIG[setting]
]

if missing_settings:
    raise RuntimeError(
        "Missing MySQL credentials in .env: "
        + ", ".join(missing_settings)
    )

# 4. Check and load the cleaned CSV
if not CSV_PATH.exists():
    raise FileNotFoundError(f"Clean CSV not found: {CSV_PATH}")

data = pd.read_csv(CSV_PATH)

if data.empty:
    raise ValueError("The clean CSV contains no records.")

required_columns = [
    "order_id",
    "order_date",
    "customer_id",
    "product_id",
    "quantity",
    "unit_price",
    "discount_pct",
    "region",
    "channel",
    "payment_status",
    "order_status",
]

missing_columns = [
    column for column in required_columns
    if column not in data.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required CSV columns: {missing_columns}"
    )

print("Rows to import:", len(data))

connection = None
cursor = None

try:
    # 5. Connect to MySQL
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # 6. Insert records, ignoring existing primary keys
    sql = """
        INSERT IGNORE INTO orders (
            order_id, order_date, customer_id, product_id,
            quantity, unit_price, discount_pct, region,
            channel, payment_status, order_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    rows = [
        tuple(None if pd.isna(value) else value for value in row)
        for row in data[required_columns].itertuples(
            index=False, name=None
        )
    ]

    cursor.executemany(sql, rows)
    connection.commit()

    print("Rows inserted:", cursor.rowcount)

    # 7. Verify the total number of records
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_rows = cursor.fetchone()[0]

    print("Total rows in MySQL:", total_rows)
    print("Data loading completed.")

except Exception:
    if connection is not None and connection.is_connected():
        connection.rollback()
    raise

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
