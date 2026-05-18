import pandas as pd

# ---------------- RBI STANDARD COLUMNS ----------------

STANDARD_COLUMNS = [
    "PAN No",
    "Name Remitter",
    "Aadhaar",
    "Beneficiary Country Code",
    "Remittance Date",
    "Purpose Code",
    "Currency Code",
    "Eq USD Amount",
    "Remarks"
]

# ---------------- COLUMN MAPPING ----------------

COLUMN_MAPPING = {

    # PAN
    "PAN No": "PAN No",
    "PAN Number": "PAN No",
    "pan remitter": "PAN No",

    # NAME
    "Name Remitter": "Name Remitter",
    "Customer name": "Name Remitter",
    "name remitter": "Name Remitter",

    # AADHAAR
    "Aadhar": "Aadhaar",
    "Aadhar NO": "Aadhaar",

    # COUNTRY
    "Beneficiary Country Code": "Beneficiary Country Code",
    "Other party country code": "Beneficiary Country Code",
    "beneficiary_country_code": "Beneficiary Country Code",

    # DATE
    "Remittance Date": "Remittance Date",
    "Bill Date": "Remittance Date",
    "date_remittance": "Remittance Date",

    # PURPOSE
    "Purpose Code": "Purpose Code",
    "Purpose": "Purpose Code",
    "purpose": "Purpose Code",

    # CURRENCY
    "Currency Code": "Currency Code",
    "Crncy": "Currency Code",
    "currency code": "Currency Code",

    # USD AMOUNT
    "Eq.USD": "Eq USD Amount",
    "Bill Amount USD": "Eq USD Amount",
    "usd amount": "Eq USD Amount",

    # REMARKS
    "Remarks": "Remarks",
    "remarks": "Remarks"
}

# ---------------- STANDARDIZE FUNCTION ----------------

def standardize_dataframe(df):

    # Rename columns
    df.rename(columns=COLUMN_MAPPING, inplace=True)

    # Keep only required columns
    available_cols = [
        col for col in STANDARD_COLUMNS
        if col in df.columns
    ]

    df = df[available_cols]

    # Add missing columns
    for col in STANDARD_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    # Reorder columns
    df = df[STANDARD_COLUMNS]

    return df

# ---------------- VALIDATION FUNCTION ----------------

def validate_row(row):

    errors = []

    # Missing Currency
    if pd.isna(row["Currency Code"]) or row["Currency Code"] == "":
        errors.append("MISSING_CURRENCY")

    # Missing PAN
    if pd.isna(row["PAN No"]) or row["PAN No"] == "":
        errors.append("MISSING_PAN")

    return ", ".join(errors)

# ---------------- MAIN ETL FUNCTION ----------------

def process_files(dcard_file, lrs_file, upi_file):

    # Read files
    dcard_df = pd.read_excel(dcard_file)
    lrs_df = pd.read_excel(lrs_file)
    upi_df = pd.read_excel(upi_file)

    # Standardize
    dcard_df = standardize_dataframe(dcard_df)
    lrs_df = standardize_dataframe(lrs_df)
    upi_df = standardize_dataframe(upi_df)

    # Merge
    all_data = pd.concat([
        dcard_df,
        lrs_df,
        upi_df
    ], ignore_index=True)

    # Validation
    all_data["Error"] = all_data.apply(validate_row, axis=1)

    # Error records
    error_df = all_data[all_data["Error"] != ""]

    # Valid records
    valid_df = all_data[all_data["Error"] == ""]

    # Aggregation
    final_df = valid_df.groupby([
        "PAN No",
        "Beneficiary Country Code",
        "Currency Code"
    ], as_index=False).agg({
        "Name Remitter": "first",
        "Aadhaar": "first",
        "Remittance Date": "first",
        "Purpose Code": "first",
        "Eq USD Amount": "sum",
        "Remarks": "first"
    })

    return final_df, error_df