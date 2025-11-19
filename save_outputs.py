import duckdb, os
os.makedirs("query_outputs", exist_ok=True)
con = duckdb.connect("capstone.duckdb")

# ensure view exists on combined parquet
con.execute("CREATE OR REPLACE VIEW fish_data AS SELECT * FROM read_parquet('parquet_files/combined_parquet.parquet')")

# save first 10 rows
con.execute("COPY (SELECT * FROM fish_data LIMIT 10) TO 'query_outputs/first_10_rows.csv' (HEADER, DELIMITER ',')")

# landed value by year
con.execute("COPY (SELECT year, SUM(landed_value) AS total_landed_value FROM fish_data GROUP BY year ORDER BY year) TO 'query_outputs/landed_value_by_year.csv' (HEADER, DELIMITER ',')")

# top 10 countries
con.execute("COPY (SELECT country AS location, SUM(landed_value) AS total_value FROM fish_data GROUP BY country ORDER BY total_value DESC LIMIT 10) TO 'query_outputs/top10_countries_by_value.csv' (HEADER, DELIMITER ',')")

# top 10 species by tonnes (use fish_name)
con.execute("COPY (SELECT fish_name AS species, SUM(tonnes) AS total_tonnes FROM fish_data GROUP BY fish_name ORDER BY total_tonnes DESC LIMIT 10) TO 'query_outputs/top10_species_by_tonnes.csv' (HEADER, DELIMITER ',')")

con.close()
print("Saved CSVs to query_outputs/")
