from google.cloud import dataproc_v1 as dataproc
from google.cloud.dataproc_v1.gapic.transports import cluster_controller_grpc_transport, job_controller_grpc_transport


def get_cluster_client(credentials, region) -> dataproc.ClusterControllerClient:
    if region == 'global':
        # Use the default gRPC global endpoints.
        dataproc_cluster_client = dataproc.ClusterControllerClient(credentials=credentials)
    else:
        # Use a regional gRPC endpoint. See:
        # https://cloud.google.com/dataproc/docs/concepts/regional-endpoints
        client_transport = (
            cluster_controller_grpc_transport.ClusterControllerGrpcTransport(
                address=f"{region}-dataproc.googleapis.com:443", credentials=credentials))
        dataproc_cluster_client = dataproc.ClusterControllerClient(transport=client_transport)
    return dataproc_cluster_client


def get_job_client(credentials, region) -> dataproc.JobControllerClient:
    if region == 'global':
        # Use the default gRPC global endpoints.
        dataproc_job_client = dataproc.JobControllerClient(credentials=credentials)
    else:
        # Use a regional gRPC endpoint. See:
        # https://cloud.google.com/dataproc/docs/concepts/regional-endpoints
        client_transport = (
            job_controller_grpc_transport.JobControllerGrpcTransport(
                address=f"{region}-dataproc.googleapis.com:443", credentials=credentials))
        dataproc_job_client = dataproc.JobControllerClient(transport=client_transport)
    return dataproc_job_client


def list_clusters(client, project, region):
    """List the details of clusters in the region."""
    print("Listing clusters")
    for cluster in client.list_clusters(project, region):
        print(('{} - {}'.format(cluster.cluster_name,
                                cluster.status.State.Name(
                                    cluster.status.state))))

    # clusters = list(client.list_clusters(project, region))
    # return clusters


def create_cluster(client, project, region, cluster_name):
    print(f"Creating cluster {cluster_name}")
    # Create the cluster config.
    cluster = {
        'project_id': project,
        'cluster_name': cluster_name,
        'config': {
            'master_config': {
                'num_instances': 1,
                'machine_type_uri': 'n1-standard-1'
            },
            'worker_config': {
                'num_instances': 2,
                'machine_type_uri': 'n1-standard-1'
            }
        }
    }

    # Create the cluster.
    operation = client.create_cluster(project, region, cluster)
    result = operation.result()

    # Output a success message.
    print(f"Cluster {result.cluster_name} up")


def delete_cluster(client, project, region, cluster_name):
    print(f"Deleting cluster {cluster_name}")
    operation = client.delete_cluster(project, region, cluster_name)
    result = operation.result()

    print(f"Cluster {cluster_name} down")


def get_cluster_id_by_name(client, project, region, cluster_name):
    """Helper function to retrieve the ID and output bucket of a cluster by
    name."""
    for cluster in client.list_clusters(project, region):
        if cluster.cluster_name == cluster_name:
            return cluster.cluster_uuid, cluster.config.config_bucket


def submit_pyspark_job(client, project, region, cluster_name, bucket_name,
                       filename):
    """Submit the Pyspark job to the cluster (assumes `filename` was uploaded
    to `bucket_name."""
    job_details = {
        'placement': {
            'cluster_name': cluster_name
        },
        'pyspark_job': {
            'main_python_file_uri': 'gs://{}/{}'.format(bucket_name, filename)
        }
    }

    result = client.submit_job(
        project_id=project, region=region, job=job_details)
    job_id = result.reference.job_id
    print('Submitted job ID {}.'.format(job_id))
    return job_id


if __name__ == '__main__':
    project_test = "sincere-bongo-264115"
    # region_test = "southamerica-east1"
    # cluster_name_test = "teste-caio"
    # list_clusters(project=project_test, region=region_test)
    # create_cluster(project=project_test, region=region_test, cluster_name=cluster_name_test)
    # list_clusters(project=project_test, region=region_test)
    # delete_cluster(project=project_test, region=region_test, cluster_name=cluster_name_test)
    # list_clusters(project=project_test, region=region_test)
