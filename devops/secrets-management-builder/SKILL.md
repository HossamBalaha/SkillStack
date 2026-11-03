---
name: secrets-management-builder
description: Build secrets management with HashiCorp Vault policies, Kubernetes External Secrets Operator, AWS Secrets Manager, and rotation schedules. Use this when the user asks to centralize secrets, replace K8s Secret manifests with external stores, or set up DB credential rotation.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [vault, secrets, external-secrets, rotation, kubernetes, aws-secrets-manager]
related: [devops/kubernetes-manifest-builder, devops/terraform-module-author]
prerequisites: [devops/kubernetes-manifest-builder]
outputs: [yaml, bash, markdown]
difficulty: advanced
estimated_tokens: 1900
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Secrets Management Builder

## When To Use

- The user says "centralize our secrets in Vault" or "stop committing K8s Secret YAML".
- The user wants Kubernetes pods to fetch secrets from Vault or AWS Secrets Manager at runtime.
- The user wants database credentials rotated on a schedule (30/90 days).
- The user wants a secrets workflow with separate read and write paths per team.
- Trigger keywords: vault, secrets-manager, external-secrets, rotation, kv-store, kubernetes-auth.

## Workflow

1. Pick the backend: HashiCorp Vault (self-hosted/cloud), AWS Secrets Manager, GCP Secret Manager, Azure Key Vault.
2. For Vault, enable the Kubernetes auth method so pods authenticate via their service account token.
3. Author policies per team: `payments-team-read` can read `secret/data/payments/*`; never grant wildcard.
4. Store secrets as KV v2 with versioned history so a rotation can be rolled back.
5. For Kubernetes, install the External Secrets Operator (ESO) and define a `SecretStore` pointing at Vault or AWS
   Secrets Manager.
6. Define `ExternalSecret` resources that map external keys to K8s Secret entries; the operator reconciles them.
7. Configure rotation: in Vault, a database secrets engine rotates the password; in AWS, a Lambda rotation function
   flips the secret and updates the DB.
8. Set rotation intervals (30 days for DB credentials, 90 days for API keys).
9. Audit access with Vault's audit log or AWS CloudTrail; alert on unexpected reads.
10. Document the break-glass procedure: how to manually rotate if automation fails.

## Inputs

- Backend choice (Vault, AWS Secrets Manager, GCP Secret Manager).
- Team names and the secret paths each team should access.
- Rotation targets (Postgres, MySQL, third-party API keys).
- Kubernetes service account for ESO and for app pods.
- Rotation interval per secret class.

## Outputs

- `vault/policies/<team>-read.hcl` — read policy.
- `vault/auth/kubernetes.yaml` — K8s auth role binding.
- `eso/secretstore.yaml` — `SecretStore` pointing at the backend.
- `eso/externalsecret-<app>.yaml` — `ExternalSecret` mapping.
- `rotation/db-engine.yaml` — Vault database engine config + role.
- `README.md` — access model, rotation schedule, break-glass steps.

## Key Rules

- Never grant `secret/data/*` wildcard; always scope policies to a team's path prefix.
- Always use KV v2, not v1; v2 has versioning and metadata for rollback.
- Pods must authenticate via Kubernetes service account, not static tokens; static tokens leak.
- Rotation must update the secret at the source (DB password) and the store in one atomic flow; partial updates break
  apps.
- External Secrets Operator should refresh on a schedule (1h default) so rotated secrets propagate.
- Audit logs must be reviewed; unexplained reads are the leading indicator of compromise.
- Break-glass rotation steps must be documented and tested quarterly.

## Examples

```hcl
# vault/policies/payments-read.hcl
path "secret/data/payments/*" {
  capabilities = ["read"]
}

path "secret/metadata/payments/*" {
  capabilities = ["read", "list"]
}

path "database/creds/payments-readonly" {
  capabilities = ["read"]
}
```

```yaml
# vault/auth/kubernetes.yaml — bind a K8s SA to a Vault role.
apiVersion: secrets.hashicorp.com/v1
kind: VaultAuth
metadata:
  name: payments
  namespace: payments
spec:
  method: kubernetes
  mount: kubernetes
  kubernetes:
    role: payments-team
    serviceAccount: payments-api
```

```yaml
# eso/externalsecret-payments.yaml
apiVersion: external-secrets.io/v1
kind: ExternalSecret
metadata:
  name: payments-secrets
  namespace: payments
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: payments-secret
    creationPolicy: Owner
  data:
    - secretKey: stripe_key
      remoteRef:
        key: payments/stripe
        property: api_key
```

```hcl
# rotation/db-engine.yaml — Vault database secrets engine rotates Postgres.
resource "vault_database_secret_backend_connection" "payments" {
  name       = "payments-postgres"
  backend    = "database"
  plugin_name = "postgresql-database-plugin"
  allowed_roles = ["payments-readonly"]
  postgresql {
    connection_url = "postgresql://{{username}}:{{password}}@db.internal:5432/payments?sslmode=require"
    username       = "vault_admin"
    password       = data.vault_kv_secret_v2.db_admin.data.value
  }
}

resource "vault_database_secret_backend_role" "readonly" {
  backend             = "database"
  name                = "payments-readonly"
  db_name             = vault_database_secret_backend_connection.payments.name
  creation_statements = ["CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";"]
  default_ttl         = "1h"
  max_ttl             = "24h"
}
```
