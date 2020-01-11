from flask import Blueprint, jsonify
import dataproc_service as dataproc_service

controllers = Blueprint("controllers", __name__, url_prefix="/api")


@controllers.route("/ping")
def ping():
    return jsonify("pong")


@controllers.route("/dataproc/list-clusters")
def dataproc_list_clusters():
    project_id = "sincere-bongo-264115"
    region = "southamerica-east1"

    return dataproc_service.list_clusters(project_id=project_id, region=region)


@controllers.route("/dataproc/create-cluster")
def dataproc_create_cluster():
    project_id = "sincere-bongo-264115"
    region = "southamerica-east1"
    cluster_name = "teste-caio"

    return dataproc_service.create_cluster(project_id=project_id, region=region, cluster_name=cluster_name)


@controllers.route("/dataproc/delete-cluster")
def dataproc_delete_cluster():
    project_id = "sincere-bongo-264115"
    region = "southamerica-east1"
    cluster_name = "teste-caio"

    return dataproc_service.delete_cluster(project_id=project_id, region=region, cluster_name=cluster_name)
