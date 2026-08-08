# MYRegionalIncome

A data pipeline that computes inflation-adjusted household income trends by
Malaysian state, using open government data from OpenDOSM.

## Live dashboard

[View on Streamlit Community Cloud](https://myregionalincome-aqxnzdehnyse68twfimnm7.streamlit.app/)

## What it answers

Did household income growth actually outpace cost-of-living increases, and
does that differ by state? Combines household income/poverty survey data
with regional CPI to compute real (inflation-adjusted) income per state,
alongside population context.

## Architecture

**Bronze → Silver → Gold**, orchestrated by Airflow, built with dbt on
DuckDB locally, with finished gold tables pushed to BigQuery.

- **Bronze** — raw data pulled from the OpenDOSM API, landed unmodified.
- **Silver** — cleaned per source: CPI filtered to the headline "overall"
  category and resampled monthly → annual; population filtered to
  state-level totals (age/sex/ethnicity breakdowns collapsed); HIES
  type-cast.
- **Gold** — `fct_state_socioeconomic`: one row per state per HIES survey
  year, joining income, population, and CPI, with real (inflation-adjusted)
  income calculated against a 2010 base.

## Tech stack

| Layer | Tool |
|---|---|
| Extract | Python (`requests`) |
| Local warehouse | DuckDB |
| Transform | dbt |
| Orchestration | Airflow (Docker) |
| Cloud warehouse | Google BigQuery (sandbox) |
| Dashboard | Streamlit + Plotly |

## Data sources

All from [OpenDOSM](https://open.dosm.gov.my/), Malaysia's open data portal:
- [Household Income & Expenditure by State](https://open.dosm.gov.my/data-catalogue/hies_state)
- [Population by State](https://open.dosm.gov.my/data-catalogue/population_state)
- [CPI by State](https://open.dosm.gov.my/data-catalogue/cpi_state)

## Known data characteristics

- HIES is survey-based, not annual — gold table only has rows for actual
  survey years (e.g. 2022, 2024), not a continuous year range.
- Population estimates lag HIES by roughly a year at the source; the most
  recent HIES year may show `null` population by design, not by bug.
- BigQuery sandbox tables expire after 60 days of inactivity.

## Setup

1. `pip install -r requirements.txt`
2. Copy `.env.example` → `.env` and fill in values
3. Copy `myregionalincome_dbt/docker_profile/profiles.yml.example` →
   `profiles.yml` and set your GCP project ID
4. `gcloud auth application-default login`
5. `python extract_data.py`
6. `python load_to_bronze.py`
7. `cd myregionalincome_dbt && dbt seed && dbt run && dbt test`
8. `python ../push_to_bigquery.py`
9. Or run the whole thing via the Airflow DAG in `dags/`