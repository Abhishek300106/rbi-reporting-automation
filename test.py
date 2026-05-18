from etl import process_files

final_df, error_df = process_files(
    "input/DCARD.xlsx",
    "input/LRS.xlsx",
    "input/UPI.xlsx"
)

print(final_df.head())
print(error_df.head())