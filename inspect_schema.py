import duckdb
con = duckdb.connect("capstone.duckdb")
# show columns for the view/table
print(con.execute("SELECT table_schema, table_name, column_name, data_type FROM information_schema.columns WHERE table_name='fish_data' ORDER BY ordinal_position").df())
con.close()
