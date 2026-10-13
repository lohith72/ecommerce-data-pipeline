
import pandas as pd
from pathlib import Path

# Locate the cleaned dataset
PROJECT_DIR = Path(__file__).resolve().parents[1]
CLEAN_FILE = PROJECT_DIR / "data" / "processed" / "clean_orders.csv"


def load_clean_data():
    """Load the cleaned orders dataset."""
    assert CLEAN_FILE.exists(), f"Clean file not found: {CLEAN_FILE}"
    return pd.read_csv(CLEAN_FILE)


def test_no_missing_values():
    df = load_clean_data()
    assert df.isnull().sum().sum() == 0


def test_no_duplicate_rows():
    df = load_clean_data()
    assert not df.duplicated().any()


def test_no_invalid_quantities():
    df = load_clean_data()
    assert (df["quantity"] > 0).all()


def test_no_invalid_unit_prices():
    df = load_clean_data()
    assert (df["unit_price"] > 0).all()


def test_no_invalid_discounts():
    df = load_clean_data()
    assert df["discount_pct"].between(0, 1).all()


def test_unique_order_ids():
    df = load_clean_data()
    assert df["order_id"].is_unique


def test_expected_row_count():
    df = load_clean_data()
    assert len(df) == 10020
