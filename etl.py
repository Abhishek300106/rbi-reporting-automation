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

# UPI FILE

"PAN_REMITTER": "PAN No",
"NAME_REMITTER": "Name Remitter",
"BENEFICIARY_COUNTRY_CODE": "Beneficiary Country Code",
"DATE_REMITTANCE": "Remittance Date",
"PURPOSE_CODE": "Purpose Code",
"CURRENCY_CODE": "Currency Code",
"USD_AMOUNT": "Eq USD Amount",
"REMARKS": "Remarks",

# DCARD VARIATIONS

"PAN no": "PAN No",
"Name Remmiter": "Name Remitter",
"AAdhar": "Aadhaar",
"Eq.USD Amount": "Eq USD Amount",

# LRS VARIATIONS

"Other Party country Code": "Beneficiary Country Code",
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

    pan = str(row["PAN No"]).strip()
    currency = str(row["Currency Code"]).strip()

    if pan == "" or pan.lower() == "nan":
        errors.append("MISSING_PAN")

    if currency == "" or currency.lower() == "nan":
        errors.append("MISSING_CURRENCY")

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

    # Merge all files
    all_data = pd.concat(
        [dcard_df, lrs_df, upi_df],
        ignore_index=True
    )

    # Validation
    all_data["Error"] = all_data.apply(
        validate_row,
        axis=1
    )

    # Error records
    error_df = all_data[
        all_data["Error"] != ""
    ]

    # Valid records
    valid_df = all_data[
        all_data["Error"] == ""
    ]

    # Aggregation
    final_df = valid_df.groupby(
        [
            "PAN No",
            "Beneficiary Country Code",
            "Currency Code"
        ],
        as_index=False
    ).agg({
        "Name Remitter": "first",
        "Aadhaar": "first",
        "Remittance Date": "first",
        "Purpose Code": "first",
        "Eq USD Amount": "sum",
        "Remarks": "first"
    })

    # Ensure exact RBI column order
    final_df = final_df[
        [
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
    ]

    return final_df, error_df


