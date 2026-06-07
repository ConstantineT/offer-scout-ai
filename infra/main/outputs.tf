output "agent_url" {
  value = var.deploy_services ? google_cloud_run_v2_service.agent[0].uri : null
}

output "coordinator_url" {
  value = var.deploy_services ? google_cloud_run_v2_service.coordinator[0].uri : null
}

output "resend_webhook_url" {
  value = var.deploy_services ? "${google_cloud_run_v2_service.coordinator[0].uri}/webhooks/resend" : null
}

output "secret_names" {
  value = sort(keys(google_secret_manager_secret.secrets))
}

output "tasks_queue_name" {
  value = google_cloud_tasks_queue.email_processing.name
}
