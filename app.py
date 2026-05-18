import streamlit as st
import pandas as pd
from etl import process_files
from io import BytesIO 
# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="RBI Reporting Automation",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
    <style>

    .main {
        background-color: #f5f7fa;
    }

    h1 {
        color: #003366;
        text-align: center;
    }

    .stButton>button {
        background-color: #b30000;
        color: white;
        border-radius: 8px;
        height: 50px;
        width: 100%;
        font-size: 18px;
    }

    .stDownloadButton>button {
        background-color: #003366;
        color: white;
        border-radius: 8px;
    }

    </style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("RBI Reporting Automation Portal")

st.write("Upload DCARD, LRS and UPI files to generate RBI reports.")

# ---------------- FILE UPLOADS ----------------

dcard_file = st.file_uploader(
    "Upload DCARD File",
    type=["xlsx"]
)

lrs_file = st.file_uploader(
    "Upload LRS File",
    type=["xlsx"]
)

upi_file = st.file_uploader(
    "Upload UPI File",
    type=["xlsx"]
)

# ---------------- PROCESS BUTTON ----------------

if st.button("Generate RBI Report"):

    if dcard_file and lrs_file and upi_file:

        # Process files
        final_df, error_df = process_files(
            dcard_file,
            lrs_file,
            upi_file
        )

        st.success("ETL Processing Completed Successfully.")

        # ---------------- FINAL FILE ----------------

        final_buffer = BytesIO()

        with pd.ExcelWriter(final_buffer, engine='openpyxl') as writer:
            final_df.to_excel(writer, index=False)

        final_buffer.seek(0)

        st.download_button(
            label="Download RBI Final File",
            data=final_buffer,
            file_name="RBI_FINAL.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # ---------------- ERROR FILE ----------------

        error_buffer = BytesIO()

        with pd.ExcelWriter(error_buffer, engine='openpyxl') as writer:
            error_df.to_excel(writer, index=False)

        error_buffer.seek(0)

        st.download_button(
            label="Download Error Report",
            data=error_buffer,
            file_name="ERROR_REPORT.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # ---------------- PREVIEW ----------------

        st.subheader("RBI Final Report Preview")

        st.dataframe(final_df.head(10))

    else:
        st.error("Please upload all 3 files.")