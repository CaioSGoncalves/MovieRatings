provider "google-beta" {
  credentials = "${file("../key_file.json")}"
  project = "sincere-bongo-264115"
  region  = "southamerica-east1"
  zone    = "southamerica-east1-b"
}

resource "google_compute_instance" "vm_instance" {
  name         = "terraform-instance"
  machine_type = "n1-standard-1"

  metadata_startup_script = "${file("./startup_script.sh")}"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
      size = 20
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }

  service_account {
    scopes = ["userinfo-email", "compute-ro", "storage-ro"]
  }
}


resource "google_storage_bucket_object" "kafka_ingestion_job" {
  name   = "movie_ratings/jobs/kafka_ingestion.py"
  source = "../jobs/kafka_ingestion.py"
  bucket = "teste-caio"
}

resource "google_storage_bucket_object" "zeppelin_init" {
  name   = "movie_ratings/zeppelin_init.sh"
  source = "./zeppelin_init.sh"
  bucket = "teste-caio"
}

resource "google_dataproc_cluster" "streaming-cluster" {
  name   = "streaming-cluster"
  region = "southamerica-east1"

  cluster_config {
    staging_bucket = "staging.sincere-bongo-264115.appspot.com"

    master_config {
        num_instances = 1
        machine_type  = "n1-standard-1"
        disk_config {
          boot_disk_type    = "pd-standard"
          boot_disk_size_gb = 100
        }
    }

    software_config {
      image_version = "1.4-debian9"
      override_properties = {
        "dataproc:dataproc.allow.zero.workers" = "true"
      }
    }

  }
}

# Submit an example pyspark job to a dataproc cluster
resource "google_dataproc_job" "pyspark" {
  region = google_dataproc_cluster.streaming-cluster.region
  force_delete = true
  placement {
    cluster_name = google_dataproc_cluster.streaming-cluster.name
  }

  pyspark_config {
    main_python_file_uri = "gs://teste-caio/movie_ratings/jobs/kafka_ingestion.py"
    properties = {
      "spark.jars.packages" = "io.delta:delta-core_2.11:0.5.0,org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.4"
    }
  }
}

resource "google_dataproc_cluster" "playground-cluster" {
  name   = "playground-cluster"
  region = "southamerica-east1"
  provider = "google-beta"
  
  cluster_config {
    staging_bucket = "staging.sincere-bongo-264115.appspot.com"

    master_config {
        num_instances = 1
        machine_type  = "n1-standard-1"
        disk_config {
          boot_disk_type    = "pd-standard"
          boot_disk_size_gb = 100
        }
    }

    software_config {
      image_version = "1.4-debian9"
      override_properties = {
        "dataproc:dataproc.allow.zero.workers" = "true"
      }
      optional_components = [ "ZEPPELIN" ]
    }

    endpoint_config {
      enable_http_port_access = "true"
    }

    initialization_action {
        script      = "gs://teste-caio/movie_ratings/zeppelin_init.sh"
        timeout_sec = 500
    }

  }

}