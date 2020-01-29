from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'start_date': datetime(2019, 1, 29),
}

dag = DAG(
    'composer_daily_job', default_args=default_args, schedule_interval="@daily")

t1 = BashOperator(
    task_id='daily_job',
    bash_command='gcloud dataproc jobs submit pyspark \
                --cluster cluster-3bff --region southamerica-east1 \
                --properties spark.jars.packages=io.delta:delta-core_2.11:0.5.0 \
                gs://teste-caio/jobs/daily_job.py',
    dag=dag)