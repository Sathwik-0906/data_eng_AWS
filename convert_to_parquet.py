import pandas as pd
import duckdb
import pyarrow.parquet as pq
import pyarrow as pa
import os

# List of the three CSV files
csv_files = [
    "SAU-GLOBAL-1-v48-0.csv",
    "SAU-HighSeas-71-v48-0.csv",
    "SAU-EEZ-242-v48-0.csv"
]

# Output directory for Parquet files
output_dir = "parquet_files"
os.makedirs(output_dir, exist_ok=True)

def clean_column_names(df):
    """
    Standardizes column names:
    - lowercase
    - replace spaces with _
    - remove special characters
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("__", "_")
    )
    return df

print("\n--- Converting CSV → Parquet ---\n")

for csv_file in csv_files:
    print(f"Processing {csv_file} ...")
    
    # Read CSV
    df = pd.read_csv(csv_file)
    
    # Clean column names
    df = clean_column_names(df)

    # Convert to Arrow Table
    table = pa.Table.from_pandas(df)

    # Write Parquet file
    parquet_path = os.path.join(output_dir, csv_file.replace(".csv", ".parquet"))
    pq.write_table(table, parquet_path)

    print(f"Saved → {parquet_path}\n")

print("All CSV files converted to Parquet successfully!")

