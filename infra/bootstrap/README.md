# Bootstrap Infrastructure

Creates one-time Google Cloud resources needed before CI/CD and the main
deployment can run.

## Apply

```bash
terraform init
terraform apply -var="project_id=<your-gcp-project-id>"
```

Use the outputs to configure GitHub repository variables:

- `GCP_PROJECT_ID`
- `GCP_REGION`
- `GCP_WORKLOAD_IDENTITY_PROVIDER`
- `GCP_SERVICE_ACCOUNT`

The main Terraform layer uses the generated GCS state bucket.
