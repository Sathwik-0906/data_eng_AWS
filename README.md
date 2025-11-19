

# 🚀 AWS Data Engineering Capstone – Local Implementation

This project is a **complete local re-creation** of the AWS Academy Data Engineering Capstone.
Since AWS lab access was inactive, the entire cloud pipeline was rebuilt using **equivalent local tools**, maintaining the same architecture and workflow found in AWS.

---

## 📌 **Project Overview**

The goal of this project is to simulate an end-to-end **data engineering pipeline** using open-source tools that match AWS services.
It processes the **SAU fishery datasets**, converts them into Parquet format, builds unified analytical tables, and performs transformations and visualizations.

---

## 🧰 **Tools & Technologies**

| AWS Service           | Local Equivalent        | Purpose                            |
| --------------------- | ----------------------- | ---------------------------------- |
| **Amazon S3**         | Local folders           | Raw + processed data storage       |
| **AWS Glue ETL**      | Python, Pandas, PyArrow | Data cleaning, transformation, ETL |
| **Glue Data Catalog** | DuckDB Views            | Schema + unified table             |
| **Amazon Athena**     | DuckDB SQL              | Analytical queries on Parquet      |
| **Amazon QuickSight** | Matplotlib              | Visualizations                     |

Additional Tools:

* **Python 3.13**
* **VS Code**

---

## 📂 **Dataset Used**

**Source:** SAU fishery datasets

* `SAU-EEZ-242-v48-0.csv`
* `SAU-GLOBAL-1-v48-0.csv`
* `SAU-HighSeas-71-v48-0.csv`

These files are stored in the `raw_data/` folder.

---

## 🔄 **End-to-End Workflow**

### **1️⃣ Data Ingestion**

* Load raw CSV files into Python
* Perform basic cleaning (missing values, types)

### **2️⃣ CSV → Parquet Conversion**

```python
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
```

* Convert all CSVs into Parquet
* Save inside `parquet_files/`

### **3️⃣ Schema Normalization**

* Standardize column names
* Fix data types
* Align schema across datasets

### **4️⃣ Dataset Merging using DuckDB**

```python
import duckdb
```

* Load Parquet files
* Create unified views (similar to Glue Catalog)
* Build final analytical table

### **5️⃣ SQL Analytical Queries**

Examples:

* Total catch by country
* Top species
* Yearly catch trends
* High Seas vs Global comparison

### **6️⃣ Visualization**

Using Matplotlib:

* Line chart for yearly trends
* Bar chart for top catch contributors
* Pie chart for species distribution

---

## 📊 **Project Architecture (Local AWS Equivalent)**

```
          RAW CSV FILES (Local Storage)
                      |
                      ▼
          Python + Pandas (ETL)
                      |
                      ▼
               Parquet Files
                      |
                      ▼
               DuckDB SQL Engine
                      |
                      ▼
              Analytics & Queries
                      |
                      ▼
               Matplotlib Charts
```

---

## 🧩 **Key Learnings**

* How to recreate cloud pipelines locally
* CSV → Parquet data optimization
* Building unified analytical datasets
* DuckDB as an alternative to AWS Athena
* End-to-end ETL + analytics pipeline design
* Performance optimization using columnar formats

---

## 📁 **Folder Structure**

```
aws_dataeng_capstone_local/
│
├── raw_data/
│   ├── SAU-EEZ-242-v48-0.csv
│   ├── SAU-GLOBAL-1-v48-0.csv
│   └── SAU-HighSeas-71-v48-0.csv
│
├── parquet_files/
│   ├── eez.parquet
│   ├── global.parquet
│   └── highseas.parquet
│
├── scripts/
│   ├── csv_to_parquet.py
│   ├── normalize_schema.py
│   ├── duckdb_queries.py
│   └── visualize.py
│
└── README.md
```

---

## 🚀 **How to Run the Project**

### **1. Install dependencies**

```bash
pip install pandas pyarrow duckdb matplotlib
```

### **2. Convert CSV → Parquet**

```bash
python scripts/csv_to_parquet.py
```

### **3. Run DuckDB SQL Queries**

```bash
python scripts/duckdb_queries.py
```

### **4. Generate Visualizations**

```bash
python scripts/visualize.py
```


