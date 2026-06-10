# Offer Scout AI

Offer Scout AI is a personal AI service for evaluating job offers against a candidate profile.

## Projects

- `scout-agent`: Kotlin/Spring Boot service that evaluates job offers with Spring AI, Groq-compatible chat, Tavily search, and Jina page fetching.
- `scout-coordinator`: Python/FastAPI service that receives Resend email webhooks, extracts email and attachment text, calls `scout-agent`, and replies through the Resend Email API.

## Local Run

Copy the environment template:

```bash
cp .env.example .env
```

Start the services:

```bash
docker compose up --build scout-agent scout-coordinator
```

Docker Compose uses only the root `.env` file. Module-local `.env` files and
`application-local.yml` are for direct local runs outside Docker Compose.

## Local Testing

- Direct agent `curl` examples are in `scout-agent/README.md`.
- Email/webhook tests are in `scout-coordinator/README.md`.
- Coordinator supports two local webhook paths:
  - webhook.site capture and replay to `localhost`.
  - ngrok forwarding from Resend to local Docker Compose.

## GCP Deployment

Production shape:

- `scout-coordinator`: public Cloud Run service for Resend webhooks, protected by Svix signature verification.
- `scout-agent`: private Cloud Run service, invoked only by coordinator using Google ID tokens.
- Cloud Tasks: async email processing after webhook acceptance.
- Secret Manager: API keys, webhook credentials, and candidate profile context.
- Artifact Registry and GitHub Actions: image build, image push, and Cloud Run revision updates.
- Cloud Run max instances default to `1` per service for this personal deployment.

Terraform lives in `infra/`:

- `infra/bootstrap`: one-time setup for APIs, Artifact Registry, Terraform state, and GitHub Actions Workload Identity Federation.
- `infra/main`: Cloud Run services, Cloud Tasks queue, Secret Manager containers, and IAM.

Manual deployment outline:

```bash
cd infra/bootstrap
terraform init
terraform apply \
  -var="project_id=<your-gcp-project-id>" \
  -var="github_owner=<your-github-owner>"
```

`github_owner` is the GitHub user or organization that owns the repository.

Then configure these GitHub repository variables from the Terraform outputs:

- `GCP_PROJECT_ID`
- `GCP_REGION`
- `GCP_WORKLOAD_IDENTITY_PROVIDER`
- `GCP_SERVICE_ACCOUNT`

Create the main infrastructure once without Cloud Run services:

```bash
cd ../main
terraform init \
  -backend-config="bucket=<project-id>-tfstate" \
  -backend-config="prefix=infra/main"
terraform apply -var="project_id=<your-gcp-project-id>"
```

Upload secret values manually:

```bash
printf "secret-value" | gcloud secrets versions add <secret-name> --data-file=-
```

Required secret names:

- `groq-api-key`
- `tavily-api-key`
- `resend-credentials`
- `profile-context`

Secret value shapes:

```json
{"api_key":"...","webhook_secret":"...","from_email":"Offer Scout <scout@your-domain>"}
```

For email use, configure a custom email domain in Resend and add the DNS
records requested by Resend at your domain provider. The same verified domain
should support receiving forwarded job-offer emails and sending replies.

`jina-api-key` is optional and is not injected unless `enable_jina_api_key=true`.

Push the deployment workflow to `main`. The first GitHub Actions deployment
pushes Docker images to Artifact Registry. If Cloud Run services do not exist
yet, it skips service updates.

The workflow also has a manual trigger in GitHub Actions. Run it from `main`
when you want to rebuild and redeploy the current main commit without creating
a new commit.

Then create Cloud Run services manually with Terraform using the pushed image
tags:

```bash
terraform apply \
  -var="project_id=<your-gcp-project-id>" \
  -var="deploy_services=true" \
  -var="agent_image=<region>-docker.pkg.dev/<project>/offer-scout-ai/scout-agent:<commit-sha>" \
  -var="coordinator_image=<region>-docker.pkg.dev/<project>/offer-scout-ai/scout-coordinator:<commit-sha>"
```

After that, future pushes to `main` update existing Cloud Run revisions without
running Terraform.

Set the Resend webhook URL to:

```text
https://<scout-coordinator-cloud-run-url>/webhooks/resend
```

## Development

See each project README for service-specific commands and architecture notes.
