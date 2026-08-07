from pathlib import Path
import duckdb
from google.cloud import bigquery

PROJECT_ID = "my-regional-income-504714"
DATASET = "gold"
DB_PATH = Path(__file__).parent / "my_regional_income.duckdb"

client = bigquery.Client(project=PROJECT_ID)
client.create_dataset(f"{PROJECT_ID}.{DATASET}", exists_ok=True)

con = duckdb.connect(str(DB_PATH))

for table in ["dim_state", "fct_state_socioeconomic"]:
    df = con.execute(f"select * from {table}").fetchdf()
    table_id = f"{PROJECT_ID}.{DATASET}.{table}"
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    print(f"Loaded {len(df)} rows into {table_id}")

con.close()