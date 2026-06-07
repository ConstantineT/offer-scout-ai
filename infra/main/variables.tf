variable "project_id" {
  description = "Google Cloud project id."
  type        = string
}

variable "region" {
  description = "Deployment region."
  type        = string
  default     = "europe-west1"
}

variable "agent_image" {
  description = "Fully qualified scout-agent container image."
  type        = string
  default     = ""
}

variable "coordinator_image" {
  description = "Fully qualified scout-coordinator container image."
  type        = string
  default     = ""
}

variable "deploy_services" {
  description = "Deploy Cloud Run services. Set false on the first apply to create secret containers before uploading secret versions."
  type        = bool
  default     = false
}

variable "agent_service_name" {
  description = "Cloud Run service name for scout-agent."
  type        = string
  default     = "scout-agent"
}

variable "coordinator_service_name" {
  description = "Cloud Run service name for scout-coordinator."
  type        = string
  default     = "scout-coordinator"
}

variable "tasks_queue_name" {
  description = "Cloud Tasks queue name."
  type        = string
  default     = "scout-email-processing"
}

variable "enable_jina_api_key" {
  description = "Inject JINA_API_KEY into scout-agent. Enable only after adding a secret version."
  type        = bool
  default     = false
}

variable "max_instance_count" {
  description = "Maximum Cloud Run instances per service."
  type        = number
  default     = 2
}
