terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.13.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials = "./keys/my-creds.json"
  project     = "nice-diorama-412708"
  region      = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "nice-diorama-412708-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}