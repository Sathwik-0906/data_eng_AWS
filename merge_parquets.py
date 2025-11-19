# merge_parquets.py
import pandas as pd
import glob, os

parquet_dir = "parquet_files"
out_file = "parquet_files/combined_parquet.parquet"

# Find parquet files
files = glob.glob(os.path.join(parquet_dir, "*.parquet"))
print("Files to merge:", files)

# A conservative mapping of variant column names -> standard names we want:
col_renames = {
    "common_name": "fish_name",
    "common name": "fish_name",
    "fishing_entity": "country",
    "fishing_entity_name": "country",  # in case
    "landings_value": "landed_value",
    "landings_value_usd": "landed_value",
    "species_common_name": "fish_name",
    "species": "fish_name"
}

dfs = []
all_cols = set()

for f in files:
    print("Reading", f)
    df = pd.read_parquet(f)
    # strip and lower column names for safe matching
    df.columns = [c.strip() for c in df.columns]
    # rename known variants
    rename_map = {}
    for c in df.columns:
        lower = c.lower()
        if lower in col_renames:
            rename_map[c] = col_renames[lower]
    if rename_map:
        df = df.rename(columns=rename_map)
        print(" Renamed columns:", rename_map)
    # record columns
    for c in df.columns:
        all_cols.add(c)
    dfs.append(df)

# Determine final column order (union of all)
all_cols = list(sorted(all_cols))
print("Union columns count:", len(all_cols))

# Reindex each df to union columns (missing columns become NaN)
aligned = []
for df in dfs:
    missing = [c for c in all_cols if c not in df.columns]
    if missing:
        # create missing cols with NaN
        for m in missing:
            df[m] = pd.NA
    # reorder
    df = df[all_cols]
    aligned.append(df)

# Concatenate
print("Concatenating dataframes...")
combined = pd.concat(aligned, ignore_index=True)

# Optional: ensure numeric columns have proper dtype
for col in ["year", "tonnes", "landed_value", "uncertainty_score"]:
    if col in combined.columns:
        combined[col] = pd.to_numeric(combined[col], errors="coerce")

# Write combined parquet
print("Writing combined parquet to", out_file)
combined.to_parquet(out_file, index=False)
print("Done. Combined rows:", len(combined))
