# Infrastructure

Terraform for deploying Offer Scout AI to Google Cloud.

## Layers

- `bootstrap`: one-time project setup, Artifact Registry, Terraform state, and GitHub Actions identity.
- `main`: Cloud Run, Cloud Tasks, Secret Manager, and IAM for the app.

Run `bootstrap` first, then configure GitHub repository variables from its
outputs, add secret versions, and run `main`.
