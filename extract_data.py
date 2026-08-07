from pathlib import Path
import requests
import pandas as pd

BASE_URL = "https://api.data.gov.my/data-catalogue"
BRONZE_DIR = Path(__file__).parent / "data" / "bronze"
BRONZE_DIR.mkdir(parents=True, exist_ok=True)


DATASETS = {
    "hies_state": "hies_state.csv",
    "population_state": "population_state.csv",
    "cpi_state": "cpi_state.csv",
}

for dataset_id, filename in DATASETS.items():
    response = requests.get(BASE_URL, params={"id": dataset_id})
    response.raise_for_status()
    df = pd.DataFrame(response.json())
    df.to_csv(BRONZE_DIR / filename, index=False)
    print(f"{dataset_id}: saved {len(df)} rows -> {BRONZE_DIR / filename}")