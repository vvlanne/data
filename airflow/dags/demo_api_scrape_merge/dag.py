from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from pipeline import fetch_posts, export_long_posts


"""
Task 3: Create dag "v1_posts_pipeline". Set start date to yesterday.

The dag should run every monday at 8PM (use cron expression in schedule).

HINT: https://crontab.guru/
"""
with DAG(
    dag_id="v1_posts_pipeline",
    start_date=datetime.now() - timedelta(days=1),
    schedule="0 20 * * 1",
) as dag:
    # define both tasks using PythonOperator
    fetch_task = PythonOperator(
        task_id="fetch_posts",
        python_callable=fetch_posts,
    )

    export_task = PythonOperator(
        task_id="export_long_posts",
        python_callable=export_long_posts,
    )

    # Dependency: first fetch, then export
    fetch_task >> export_task
