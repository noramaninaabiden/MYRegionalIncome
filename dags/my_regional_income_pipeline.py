from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="my_regional_income_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    extract = BashOperator(
        task_id="extract_data",
        bash_command="python /opt/airflow/portfolio/MYRegionalIncome/extract_data.py",
    )

    load_bronze = BashOperator(
        task_id="load_bronze",
        bash_command="python /opt/airflow/portfolio/MYRegionalIncome/load_to_bronze.py",
    )

    dbt_seed = BashOperator(
        task_id="dbt_seed",
        bash_command="dbt seed --project-dir /opt/airflow/portfolio/MYRegionalIncome/myregionalincome_dbt --profiles-dir /opt/airflow/portfolio/MYRegionalIncome/myregionalincome_dbt/docker_profile",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="dbt run --project-dir /opt/airflow/portfolio/MYRegionalIncome/myregionalincome_dbt --profiles-dir /opt/airflow/portfolio/MYRegionalIncome/myregionalincome_dbt/docker_profile",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="dbt test --project-dir /opt/airflow/portfolio/MYRegionalIncome/myregionalincome_dbt --profiles-dir /opt/airflow/portfolio/MYRegionalIncome/myregionalincome_dbt/docker_profile",
    )

    push_to_bigquery = BashOperator(
    task_id="push_to_bigquery",
    bash_command="python /opt/airflow/portfolio/MYRegionalIncome/push_to_bigquery.py",
)

    extract >> load_bronze >> dbt_seed >> dbt_run >> dbt_test >> push_to_bigquery
