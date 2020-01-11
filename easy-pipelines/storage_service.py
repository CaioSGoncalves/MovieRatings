import os

from google.cloud import storage


DEFAULT_FILENAME = "pyspark_sort.py"


def get_storage_client(credentials) -> storage.Client:
    return storage.Client(credentials=credentials, project=credentials.project_id)


def get_pyspark_file(pyspark_file=None):
    if pyspark_file:
        f = open(pyspark_file, "rb")
        return f, os.path.basename(pyspark_file)
    else:
        """Gets the PySpark file from current directory."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        f = open(os.path.join(current_dir, DEFAULT_FILENAME), "rb")
        return f, DEFAULT_FILENAME


def upload_pyspark_file(client, bucket_name, filename, spark_file, project):
    """Uploads the PySpark file in this directory to the configured input
    bucket."""
    print('Uploading pyspark file to Cloud Storage.')
    bucket = client.bucket(bucket_name=bucket_name, user_project=project)
    blob = bucket.blob(filename)
    blob.upload_from_file(spark_file)


def download_output(client, cluster_id, output_bucket, job_id):
    """Downloads the output file from Cloud Storage and returns it as a
    string."""
    print('Downloading output file.')
    bucket = client.get_bucket(output_bucket)
    output_blob = (
        ('google-cloud-dataproc-metainfo/{}/jobs/{}/driveroutput.000000000'.
            format(cluster_id, job_id)))
    return bucket.blob(output_blob).download_as_string()


if __name__ == '__main__':
    project_test = "sincere-bongo-264115"
    bucket_name_test = "caio-teste"
    # upload_pyspark_file(credentials, bucket_name=bucket_name_test)