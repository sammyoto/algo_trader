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
                google_project_iam_binding.cloud_run_binding]

  # Autoscaling configuration
  scaling {
    min_instance_count = 1
  }

  template {
    service_account = google_service_account.schwab_algo_trader_sa.email
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

