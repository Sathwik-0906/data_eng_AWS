# query_combined.py  (fixed)
import duckdb
import os
import pandas as pd

combined = "parquet_files/combined_parquet.parquet"
out_dir = "query_outputs"
os.makedirs(out_dir, exist_ok=True)

con = duckdb.connect("capstone.duckdb")

# Use f-string to place the path directly in the SQL (avoids the prepared-parameter issue)
con.execute(f"CREATE OR REPLACE VIEW fish_data AS SELECT * FROM read_parquet('{combined}')")
print("View 'fish_data' created from combined file.")

# Show columns
print("\nCOLUMNS:")
print(con.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='fish_data' ORDER BY ordinal_position").df())

# Sample rows (only 10 rows so terminal won't overflow)
print("\n-- First 10 rows --")
print(con.execute("SELECT * FROM fish_data LIMIT 10").df())

# Total landed value by year (limit output to first 50 years)
print("\n-- Total landed value by year --")
print(con.execute("""
    SELECT year, SUM(landed_value) AS total_landed_value
    FROM fish_data
    GROUP BY year
    ORDER BY year
    LIMIT 50
""").df())

# Top 10 reporting countries by total landed value (choose existing column)
cols = [r[0] for r in con.execute("SELECT column_name FROM information_schema.columns WHERE table_name='fish_data'").fetchall()]
group_col = "country" if "country" in cols else ("area_name" if "area_name" in cols else cols[0])
print("\n-- Top 10 countries by landed value -- (grouping by:", group_col, ")")
print(con.execute(f"""
    SELECT {group_col} AS location, SUM(landed_value) AS total_value
    FROM fish_data
    GROUP BY {group_col}
    ORDER BY total_value DESC
    LIMIT 10
""").df())

# Top 10 species by tonnes
print("\n-- Top 10 species by tonnes --")
if "fish_name" in cols:
    print(con.execute("""
        SELECT fish_name AS species, SUM(tonnes) AS total_tonnes
        FROM fish_data
        GROUP BY fish_name
        ORDER BY total_tonnes DESC
        LIMIT 10
    """).df())
else:
    print("No fish_name column found; available columns:", cols)

# Optionally save results to CSV (uncomment if you want files)
# con.execute("COPY (SELECT * FROM fish_data LIMIT 10) TO 'query_outputs/first_10_rows.csv' (HEADER, DELIMITER ',');")
# con.execute("COPY (SELECT year, SUM(landed_value) AS total_landed_value FROM fish_data GROUP BY year ORDER BY year) TO 'query_outputs/landed_value_by_year.csv' (HEADER, DELIMITER ',');")

con.close()
print("\nDone.")
