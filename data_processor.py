import pandas as pd
from monday_client import fetch_deals, fetch_work_orders


def load_deals_dataframe():

    deals = fetch_deals()

    df = pd.DataFrame(deals)

    # Convert deal value to numeric
    if "Masked Deal value" in df.columns:
        df["Masked Deal value"] = pd.to_numeric(
            df["Masked Deal value"], errors="coerce"
        )

    # Convert date columns
    if "Tentative Close Date" in df.columns:
        df["Tentative Close Date"] = pd.to_datetime(
            df["Tentative Close Date"], errors="coerce"
        )

    if "Created Date" in df.columns:
        df["Created Date"] = pd.to_datetime(
            df["Created Date"], errors="coerce"
        )

    # Fill missing sector values
    if "Sector/service" in df.columns:
        df["Sector/service"] = df["Sector/service"].fillna("Unknown")

    return df


def load_work_orders_dataframe():

    work_orders = fetch_work_orders()

    df = pd.DataFrame(work_orders)

    # Convert financial columns
    money_columns = [
        "Amount in Rupees (Excl of GST) (Masked)",
        "Amount in Rupees (Incl of GST) (Masked)",
        "Amount Receivable (Masked)"
    ]

    for col in money_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert date columns
    date_columns = [
        "Probable Start Date",
        "Probable End Date",
        "Data Delivery Date",
        "Date of PO/LOI"
    ]

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


if __name__ == "__main__":

    print("\nLoading Deals DataFrame...\n")
    deals_df = load_deals_dataframe()
    print(deals_df.head())

    print("\nLoading Work Orders DataFrame...\n")
    work_orders_df = load_work_orders_dataframe()
    print(work_orders_df.head())