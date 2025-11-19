import duckdb
import os
import glob
import pandas as pd

parquet_dir = "parquet_files"
out_dir = "query_outputs"
os.makedirs(out_dir, exist_ok=True)

# Connect
con = duckdb.connect("capstone.duckdb")

# Create view combining all parquet files
con.execute("CREATE OR REPLACE VIEW fish_data AS SELECT * FROM read_parquet('parquet_files/*.parquet')")

# 1) Inspect columns (confirm)
cols = con.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='fish_data' ORDER BY ordinal_position").df()
print("COLUMNS:\n", cols)

# 2) First 10 rows
df_head = con.execute("SELECT * FROM fish_data LIMIT 10").df()
print("\n-- First 10 rows --")
print(df_head)
df_head.to_csv(os.path.join(out_dir, "first_10_rows.csv"), index=False)

# 3) Total landed value by year
q1 = """
SELECT year, SUM(landed_value) AS total_landed_value
FROM fish_data
GROUP BY year
ORDER BY year
"""
df_by_year = con.execute(q1).df()
print("\n-- Total landed value by year (sample) --")
print(df_by_year.head(20))
df_by_year.to_csv(os.path.join(out_dir, "landed_value_by_year.csv"), index=False)

# 4) Top 10 reporting countries by total landed value
q2 = """
SELECT country, SUM(landed_value) AS total_value
FROM fish_data
GROUP BY country
ORDER BY total_value DESC
LIMIT 10
"""
df_top_countries = con.execute(q2).df()
print("\n-- Top 10 countries by landed value --")
print(df_top_countries)
df_top_countries.to_csv(os.path.join(out_dir, "top10_countries_by_value.csv"), index=False)

# 5) Top 10 species by tonnes caught
q3 = """
SELECT fish_name AS species, SUM(tonnes) AS total_tonnes
FROM fish_data
GROUP BY fish_name
ORDER BY total_tonnes DESC
LIMIT 10
"""
df_top_species = con.execute(q3).df()
print("\n-- Top 10 species by tonnes --")
print(df_top_species)
df_top_species.to_csv(os.path.join(out_dir, "top10_species_by_tonnes.csv"), index=False)

# 6) Example: Fiji total value since 2001
q4 = """
SELECT year, SUM(landed_value) AS fiji_value
FROM fish_data
WHERE area_name = 'Fiji' AND year >= 2001
GROUP BY year
ORDER BY year
"""
df_fiji = con.execute(q4).df()
print("\n-- Fiji: landed value since 2001 --")
print(df_fiji.head(20))
df_fiji.to_csv(os.path.join(out_dir, "fiji_value_since_2001.csv"), index=False)

con.close()
print("\nOutputs saved to folder:", out_dir)
