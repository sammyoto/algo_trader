# Create service account and add permissions
resource "google_service_account" "schwab_algo_trader_sa" {
  account_id   = "schwab-algo-trader"
  display_name = "Schwab Algo Trading Service Account"
}

resource "google_project_iam_binding" "cloud_run_binding" {
  project = var.project_id
  role    = "roles/run.admin"
  depends_on = [google_service_account.schwab_algo_trader_sa]

  members = [
    "serviceAccount:${google_service_account.schwab_algo_trader_sa.email}",
  ]
}

resource "google_project_iam_binding" "artifact_registry_binding" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  depends_on = [google_service_account.schwab_algo_trader_sa]

  members = [
    "serviceAccount:${google_service_account.schwab_algo_trader_sa.email}",
  ]
}

resource "google_project_iam_binding" "secret_accessor_binding" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  depends_on = [google_service_account.schwab_algo_trader_sa]

  members = [
    "serviceAccount:${google_service_account.schwab_algo_trader_sa.email}",
  ]
}

# Allow Cloud Run's service account to access the bucket
resource "google_project_iam_binding" "bucket_access" {
  project = var.project_id
  role   = "roles/storage.objectAdmin"
  depends_on = [google_service_account.schwab_algo_trader_sa]

  members = [
    "serviceAccount:${google_service_account.schwab_algo_trader_sa.email}"
  ]
}

# Create a Google Cloud Storage Bucket
resource "google_storage_bucket" "trader_bucket" {
  name          = "trader-bucket-61423"
  location      = "US"
  storage_class = "STANDARD"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }

  uniform_bucket_level_access = true
}

# Upload the JSON file to the bucket
resource "google_storage_bucket_object" "state_json" {
  name   = "state.json"           # The name of the object in the bucket
  bucket = google_storage_bucket.trader_bucket.name
  source = "state.json"  # The local file to upload
}

resource "google_cloud_run_service_iam_member" "allow_public_access" {
  service = google_cloud_run_v2_service.schwab_algo_trader.id
  location = google_cloud_run_v2_service.schwab_algo_trader.location
  role    = "roles/run.invoker"
  member  = "allUsers"
  depends_on = [google_cloud_run_v2_service.schwab_algo_trader]
}

# Deploy cloud run instance
resource "google_cloud_run_v2_service" "schwab_algo_trader" {
  name     = "schwab-algo-trader"
  location = var.region
  deletion_protection = false
  ingress = "INGRESS_TRAFFIC_ALL"
  depends_on = [google_project_iam_binding.secret_accessor_binding, 
                google_project_iam_binding.artifact_registry_binding,
                google_project_iam_binding.cloud_run_binding,
                google_storage_bucket_object.state_json]

  # Autoscaling configuration
  scaling {
    min_instance_count = 1
  }

  template {
    service_account = google_service_account.schwab_algo_trader_sa.email
    timeout = "100s"
    containers {
      image = "us-central1-docker.pkg.dev/schwab-algo-trading/algo-trading/algo-trader:latest"
      resources {
        limits = {
          cpu    = "2"
          memory = "1024Mi"
        }
      }
      env {
        name = "APP_KEY"
        value_source {
          secret_key_ref {
            secret  = "schwab-app-key"
            version = "latest"
          }
        }
      }
      env {
        name = "SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = "schwab-secret-key"
            version = "latest"
          }
        }
      }
      env {
        name = "TOKENS"
        value_source {
          secret_key_ref {
            secret  = "schwab-tokens"
            version = "latest"
          }
        }
      }
    }
  }
}

#-----------------------CLOUD SCHEDULER-------------------------#

# Service account for Cloud Scheduler
resource "google_service_account" "scheduler_updater" {
  account_id   = "cloud-scheduler-updater"
  display_name = "Cloud Scheduler Updater Service Account"
}

# IAM binding for Cloud Run Admin role
resource "google_project_iam_member" "scheduler_cloud_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.scheduler_updater.email}"
}

# IAM binding for using the service account
resource "google_project_iam_member" "scheduler_service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${google_service_account.scheduler_updater.email}"
}

# Scheduler job for market open
resource "google_cloud_scheduler_job" "market_open_scaler" {
  name     = "market-open-scaler"
  schedule = "0 7 * * 1-5"  # Adjust for market open time in MST
  time_zone = "MST"

  http_target {
    http_method = "PATCH"
    uri         = "https://run.googleapis.com/v2/projects/${var.project_id}/locations/${var.region}/services/${google_cloud_run_v2_service.schwab_algo_trader.name}"
    
    oidc_token {
      service_account_email = google_service_account.scheduler_updater.email
    }

    headers = {
      "Content-Type" = "application/json"
    }

    body = base64encode(jsonencode({
      template = {
        scaling = {
          minInstanceCount = 1
        }
      }
    }))
  }
}

# Scheduler job for market close
resource "google_cloud_scheduler_job" "market_close_scaler" {
  name     = "market-close-scaler"
  schedule = "0 14 * * 1-5"  # Adjust for market close time in MST
  time_zone = "MST"

  http_target {
    http_method = "PATCH"
    uri         = "https://run.googleapis.com/v2/projects/${var.project_id}/locations/${var.region}/services/${google_cloud_run_v2_service.schwab_algo_trader.name}"
    
    oidc_token {
      service_account_email = google_service_account.scheduler_updater.email
    }

    headers = {
      "Content-Type" = "application/json"
    }

    body = base64encode(jsonencode({
      template = {
        scaling = {
          minInstanceCount = 0
        }
      }
    }))
  }
}

