provider "google" {
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
      size = "15"
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