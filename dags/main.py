from airflow import DAG
from airflow.models import Variable
from airflow.contrib.operators.dataproc_operator import DataprocClusterCreateOperator, DataProcPySparkOperator, DataprocClusterDeleteOperator

from datetime import datetime, timedelta


default_args = {
    'start_date': datetime(2020, 5, 11) # datetime(2020, 5, 1),
}

dag = DAG(
    'submit_job', default_args=default_args, schedule_interval="@once")

t1 = DataprocClusterCreateOperator(
    task_id="create_cluster",
    gcp_conn_id='google_cloud_default',
    project_id='sincere-bongo-264115',
    region='southamerica-east1',
    zone='southamerica-east1-a',
    cluster_name="airflow-cluster",
    storage_bucket='staging.sincere-bongo-264115.appspot.com',
    num_workers=0,
    master_machine_type='n1-standard-2',
    dag=dag)

t2 = DataProcPySparkOperator(
    task_id="run",
    gcp_conn_id='google_cloud_default',
    main="gs://teste-caio/movie_ratings/jobs/daily_job.py",
    job_name='test',
    cluster_name="test-cluster",
    region='southamerica-east1',
    dag=dag)


t3 = DataprocClusterDeleteOperator(
    task_id='delete_cluster',
    project_id='sincere-bongo-264115',
    cluster_name='test-cluster',
    region='southamerica-east1',
    dag=dag)

t1 >> t2 >> t3