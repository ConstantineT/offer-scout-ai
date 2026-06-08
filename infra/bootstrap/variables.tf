variable "project_id" {
  description = "Google Cloud project id."
  type        = string
}

variable "region" {
  description = "Default deployment region."
  type        = string
  default     = "europe-west1"
}

variable "github_owner" {
  description = "GitHub organization or user that owns the repository."
  type        = string
  default     = "Kotryos"
}

variable "github_repo" {
  description = "GitHub repository name."
  type        = string
  default     = "offer-scout-ai"
}

variable "artifact_repository_id" {
  description = "Artifact Registry Docker repository id."
  type        = string
  default     = "offer-scout-ai"
}

variable "state_bucket_name" {
  description = "Optional Terraform state bucket name. Defaults to <project-id>-tfstate."
  type        = string
  default     = ""
}
