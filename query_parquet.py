import duckdb
import os
import glob

# Directory containing parquet files
parquet_dir = "parquet_files"

# Find all parquet files
parquet_files = glob.glob(os.path.join(parquet_dir, "*.parquet"))

print("Parquet files found:", parquet_files)

# Connect to DuckDB
con = duckdb.connect(database="capstone.duckdb")

# Register all files as one logical table
con.execute("""
    CREATE OR REPLACE VIEW fish_data AS
    SELECT * FROM read_parquet('parquet_files/*.parquet')
""")

print("\nView 'fish_data' created combining all parquet files.")

# ------------------ SAMPLE QUERIES ------------------

print("\n--- SAMPLE QUERY 1: First 10 rows ---")
print(con.execute("SELECT * FROM fish_data LIMIT 10").df())

print("\n--- SAMPLE QUERY 2: Total fish value per year ---")
print(con.execute("""
    SELECT year, SUM(landed_value_usd) AS total_value
    FROM fish_data
    GROUP BY year
    ORDER BY year
""").df())

print("\n--- SAMPLE QUERY 3: Top 10 countries by value ---")
print(con.execute("""
    SELECT country, SUM(landed_value_usd) AS total_value
    FROM fish_data
    GROUP BY country
    ORDER BY total_value DESC
    LIMIT 10
""").df())

print("\n--- SAMPLE QUERY 4: Top 10 species by tonnes caught ---")
print(con.execute("""
    SELECT species_common_name AS species, SUM(tonnes) AS total_tonnes
    FROM fish_data
    GROUP BY species_common_name
    ORDER BY total_tonnes DESC
    LIMIT 10
""").df())

print("\nQueries finished.")
con.close()
