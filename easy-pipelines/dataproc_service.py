from google.cloud import dataproc_v1 as dataproc
from google.cloud.dataproc_v1.gapic.transports import cluster_controller_grpc_transport


def get_dataproc_client(region):
    if region == 'global':
        # Use the default gRPC global endpoints.
        dataproc_cluster_client = dataproc.ClusterControllerClient()
    else:
        # Use a regional gRPC endpoint. See:
        # https://cloud.google.com/dataproc/docs/concepts/regional-endpoints
        client_transport = (
            cluster_controller_grpc_transport.ClusterControllerGrpcTransport(
                address='{}-dataproc.googleapis.com:443'.format(region)))
        dataproc_cluster_client = dataproc.ClusterControllerClient(
            client_transport)
    return dataproc_cluster_client


def handle_client_by_region(f):
    def wrapper(*args, **kwargs):
        region = kwargs.get("region")
        client = get_dataproc_client(region)
        kwargs.update({"client": client})
        f(*args, **kwargs)

    return wrapper


@handle_client_by_region
def list_clusters(project_id, region, client):
    """List the details of clusters in the region."""
    print("Listing clusters")
    for cluster in client.list_clusters(project_id, region):
        print(('{} - {}'.format(cluster.cluster_name,
                                cluster.status.State.Name(
                                    cluster.status.state))))

    # clusters = list(client.list_clusters(project_id, region))
    # return clusters


@handle_client_by_region
def create_cluster(project_id, region, cluster_name, client):
    print(f"Creating cluster {cluster_name}")
    # Create the cluster config.
    cluster = {
        'project_id': project_id,
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
    operation = client.create_cluster(project_id, region, cluster)
    result = operation.result()

    # Output a success message.
    print(f"Cluster {result.cluster_name} up")


@handle_client_by_region
def delete_cluster(project_id, region, cluster_name, client):
    print(f"Deleting cluster {cluster_name}")
    operation = client.delete_cluster(project_id, region, cluster_name)
    result = operation.result()

    print(f"Cluster {cluster_name} down")


if __name__ == '__main__':
    project_id = "sincere-bongo-264115"
    region = "southamerica-east1"
    cluster_name = "teste-caio"
    list_clusters(project_id=project_id, region=region)
    create_cluster(project_id=project_id, region=region, cluster_name=cluster_name)
    list_clusters(project_id=project_id, region=region)
    delete_cluster(project_id=project_id, region=region, cluster_name=cluster_name)
    list_clusters(project_id=project_id, region=region)
