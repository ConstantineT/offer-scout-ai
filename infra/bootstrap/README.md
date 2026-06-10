# Bootstrap Infrastructure

Creates one-time Google Cloud resources needed before CI/CD and the main
deployment can run.

The GitHub deployer is intentionally limited. It can push Docker images and
update existing Cloud Run services, but it does not manage Terraform
infrastructure.

## Apply

```bash
terraform init
terraform apply \
  -var="project_id=<your-gcp-project-id>" \
  -var="github_owner=<your-github-owner>"
```

`github_owner` is the GitHub user or organization that owns the repository.
It is not secret, but it is deployment-specific and therefore has no default.

Use the outputs to configure GitHub repository variables:

- `GCP_PROJECT_ID`
- `GCP_REGION`
- `GCP_WORKLOAD_IDENTITY_PROVIDER`
- `GCP_SERVICE_ACCOUNT`

The main Terraform layer uses the generated GCS state bucket.
