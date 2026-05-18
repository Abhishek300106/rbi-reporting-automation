import pandas as pd
import os

# ---------------- CREATE OUTPUT FOLDER ----------------

os.makedirs("output", exist_ok=True)

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

# ---------------- FUNCTION TO STANDARDIZE FILE ----------------

def standardize_file(file_path):

    df = pd.read_excel(file_path)

    # Rename columns using mapping
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

# ---------------- READ AND STANDARDIZE FILES ----------------

dcard_df = standardize_file("input/DCARD.xlsx")
lrs_df = standardize_file("input/LRS.xlsx")
upi_df = standardize_file("input/UPI.xlsx")

# ---------------- MERGE FILES ----------------

all_data = pd.concat([
    dcard_df,
    lrs_df,
    upi_df
], ignore_index=True)

# ---------------- VALIDATION ----------------

error_rows = []

def validate_row(row):

    errors = []

    # Missing Currency Code
    if pd.isna(row["Currency Code"]) or row["Currency Code"] == "":
        errors.append("MISSING_CURRENCY")

    # Missing PAN
    if pd.isna(row["PAN No"]) or row["PAN No"] == "":
        errors.append("MISSING_PAN")

    return ", ".join(errors)

# Apply validation
all_data["Error"] = all_data.apply(validate_row, axis=1)

# Store error rows
error_rows = all_data[all_data["Error"] != ""]

# ---------------- AGGREGATION ----------------

valid_data = all_data[all_data["Error"] == ""]

final_df = valid_data.groupby([
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

# ---------------- EXPORT FILES ----------------

final_output = "output/RBI_FINAL.xlsx"
error_output = "output/ERROR_REPORT.xlsx"

final_df.to_excel(final_output, index=False)
error_rows.to_excel(error_output, index=False)

# ---------------- SUCCESS MESSAGE ----------------

print("ETL Processing Completed Successfully.")
print(f"RBI Final File: {final_output}")
print(f"Error Report: {error_output}")