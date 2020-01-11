from flask import Blueprint, jsonify
import dataproc_service
import storage_service

controllers = Blueprint("controllers", __name__, url_prefix="/api")


@controllers.route("/ping")
def ping():
    return jsonify("pong")


@controllers.route("/dataproc/list-clusters")
def execute_job():
    project = "sincere-bongo-264115"
    region = "southamerica-east1"
    cluster_name = "teste-caio"
    bucket_name = "teste-caio"
    spark_file = storage_service.get_pyspark_file()
    filename = "filename"

    storage_service.upload_pyspark_file(project, bucket_name, spark_file, filename)
    dataproc_service.create_cluster(project, region, cluster_name)
    job_result = None # dataproc_service.submit_pyspark_job(project, region, cluster_name, bucket_name, spark_filename)
    dataproc_service.delete_cluster(project, region, cluster_name)

    return job_result


# Dataproc

@controllers.route("/dataproc/list-clusters")
def dataproc_list_clusters():
    project = "sincere-bongo-264115"
    region = "southamerica-east1"

    return dataproc_service.list_clusters(project, region)


@controllers.route("/dataproc/create-cluster")
def dataproc_create_cluster():
    project = "sincere-bongo-264115"
    region = "southamerica-east1"
    cluster_name = "teste-caio"

    return dataproc_service.create_cluster(project, region, cluster_name)


@controllers.route("/dataproc/delete-cluster")
def dataproc_delete_cluster():
    project = "sincere-bongo-264115"
    region = "southamerica-east1"
    cluster_name = "teste-caio"

    return dataproc_service.delete_cluster(project, region, cluster_name)


# end

# Storage

@controllers.route("/storage/upload-pyspark-file")
def storage_upload_pyspark_file():
    project = "sincere-bongo-264115"
    bucket_name = "teste-caio"
    spark_file = "spark_file"
    filename = "filename"
    return storage_service.upload_pyspark_file(project, bucket_name, spark_file,
                                               filename)

# end
