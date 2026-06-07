output "artifact_repository" {
  value = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_repository_id}"
}

output "github_deployer_service_account" {
  value = google_service_account.github_deployer.email
}

output "state_bucket_name" {
  value = google_storage_bucket.terraform_state.name
}

output "workload_identity_provider" {
  value = google_iam_workload_identity_pool_provider.github.name
}
