# Main Infrastructure

Deploys the Offer Scout AI services.

## Initialize

Use the state bucket created by `infra/bootstrap`:

```bash
terraform init \
  -backend-config="bucket=<project-id>-tfstate" \
  -backend-config="prefix=infra/main"
```

## Secret Values

Terraform creates secret containers only. Add values manually before applying
Cloud Run services:

```bash
printf "secret-value" | gcloud secrets versions add groq-api-key --data-file=-
```

Required secret names:

- `groq-api-key`
- `tavily-api-key`
- `resend-credentials`
- `gmail-smtp-credentials`
- `profile-context`

Secret value shapes:

```json
{"api_key":"...","webhook_secret":"..."}
```

```json
{"username":"gmail@example.com","app_password":"..."}
```

Optional:

- `jina-api-key`

`jina-api-key` is not injected into `scout-agent` unless
`enable_jina_api_key=true`.

## Apply

First apply creates service accounts, secret containers, IAM, and the task
queue. It intentionally does not deploy Cloud Run yet:

```bash
terraform apply \
  -var="project_id=<your-gcp-project-id>"
```

After adding secret versions, push the deployment workflow to `main` so GitHub
Actions builds and pushes images to Artifact Registry. The first workflow run
will skip Cloud Run updates if services do not exist yet.

Then deploy the services manually with the pushed image tags:

```bash
terraform apply \
  -var="project_id=<your-gcp-project-id>" \
  -var="deploy_services=true" \
  -var="agent_image=<region>-docker.pkg.dev/<project>/offer-scout-ai/scout-agent:<tag>" \
  -var="coordinator_image=<region>-docker.pkg.dev/<project>/offer-scout-ai/scout-coordinator:<tag>"
```

After apply, set the Resend webhook URL to the `resend_webhook_url` output.

Future pushes to `main` update existing Cloud Run service images through
GitHub Actions. Terraform remains a manual Cloud Shell operation for
infrastructure changes.
