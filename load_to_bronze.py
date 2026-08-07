from pathlib import Path
import duckdb

BRONZE_DIR = Path(__file__).parent / "data" / "bronze"
BRONZE_DIR.mkdir(parents=True, exist_ok=True)

con = duckdb.connect("my_regional_income.duckdb")
con.execute("CREATE SCHEMA IF NOT EXISTS bronze")

for table in ["hies_state", "population_state", "cpi_state"]:
    con.execute(f"""
        CREATE OR REPLACE TABLE bronze.{table} AS
        SELECT * FROM read_csv_auto('{BRONZE_DIR / table}.csv')
    """)

print(con.execute("SHOW ALL TABLES").fetchdf())