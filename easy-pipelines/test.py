from google.oauth2 import service_account

import dataproc_service
import storage_service


key_path = "/home/caiosgon3/keyfile.json"
credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

project = "sincere-bongo-264115"
region = "southamerica-east1"
cluster_name = "teste-caio"
bucket_name = "teste-caio"
spark_filename = "pyspark_sort.py"
spark_file, _ = storage_service.get_pyspark_file()

cluster_client = dataproc_service.get_cluster_client(credentials, region)
job_client = dataproc_service.get_job_client(credentials, region)
storage_client = storage_service.get_storage_client(credentials)

# storage_service.upload_pyspark_file(storage_client, bucket_name, spark_filename, spark_file, project)
# dataproc_service.create_cluster(cluster_client, project, region, cluster_name)
dataproc_service.submit_pyspark_job(job_client, project, region, cluster_name, bucket_name, spark_filename)
dataproc_service.delete_cluster(cluster_client, project, region, cluster_name)

print("ACABOU")