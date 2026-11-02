---
name: terraform-module-author
description: Author reusable Terraform modules with variables.tf, main.tf, outputs.tf, versions.tf, and a README following the standard module structure. Use this when the user asks to write IaC for AWS/GCP/Azure, factor a stack into modules, or publish a module to the Terraform Registry.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [terraform, iac, module, variables, outputs, aws]
related: [devops/secrets-management-builder, devops/ci-cd-pipeline-builder]
prerequisites: []
outputs: [markdown, yaml]
difficulty: intermediate
estimated_tokens: 1600
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Terraform Module Author

## When To Use

- The user says "write a Terraform module for an S3 bucket" or "refactor this monolithic main.tf into modules".
- The user wants the standard module layout: variables, main, outputs, versions, README.
- The user is preparing to publish a module to the Terraform Registry.
- Trigger keywords: terraform, module, variables.tf, outputs.tf, terraform init, terraform plan, IaC.

## Workflow

1. Create the module directory and the five canonical files: `variables.tf`, `main.tf`, `outputs.tf`, `versions.tf`,
   `README.md`.
2. In `versions.tf`, pin `required_version` and `required_providers` with `source` and a `>=` minor bound.
3. In `variables.tf`, declare every input with `type`, `description`, and `default` (or mark `nullable = false` for
   required inputs).
4. In `main.tf`, compose provider resources, data sources, and `dynamic` blocks for repeated config; never hardcode
   values that should be variables.
5. Use locals for derived values that don't deserve a variable (e.g., name prefix with a random suffix).
6. In `outputs.tf`, expose every value downstream modules or users will need (IDs, ARNs, endpoints).
7. Tag resources consistently using a `tags` variable merged with a `Name` and `Environment` tag.
8. Author `README.md` with a usage example, an inputs table, and an outputs table (use `terraform-docs` to generate).
9. Validate with `terraform fmt`, `terraform validate`, and `terraform plan` against a scratch workspace.
10. Add an `examples/` directory with at least one runnable example.

## Inputs

- Cloud provider (aws, azurerm, google, kubernetes, etc.).
- Resource list and required inputs (e.g., bucket name, VPC CIDR, region).
- Tagging convention and naming prefix.
- Terraform minimum version and provider version constraints.

## Outputs

- `versions.tf` — `required_version` and `required_providers` block.
- `variables.tf` — input declarations.
- `main.tf` — resources and data sources.
- `outputs.tf` — exported values.
- `README.md` — usage, inputs table, outputs table.
- `examples/usage/main.tf` — runnable example.

## Key Rules

- Never hardcode values that vary by environment; promote them to variables with descriptions.
- Pin provider versions with `>=` minor bound; never use a wide `~>` for major-version safety.
- Always set `description` on every variable and output; modules without docs are unusable.
- Use `validation` blocks on variables for invariants (e.g., CIDR must be valid).
- Mark sensitive outputs with `sensitive = true` so they don't print in plan output.
- Do not store state inside the module directory; assume remote state in the consuming root.
- Run `terraform fmt -recursive` before every commit so diffs stay minimal.

## Examples

```hcl
# versions.tf
terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 6.0"
    }
  }
}
```

```hcl
# variables.tf
variable "bucket_name" {
  type        = string
  description = "Globally unique name for the S3 bucket."
  nullable    = false
  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "bucket_name must be 3-63 chars, lowercase, DNS-compatible."
  }
}

variable "tags" {
  type        = map(string)
  description = "Tags applied to all resources."
  default     = {}
}
```

```hcl
# main.tf
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
  tags = merge(var.tags, {
    Name    = var.bucket_name
    Module  = "tf-s3-bucket"
    Managed = "terraform"
  })
}

resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

```hcl
# outputs.tf
output "bucket_arn" {
  value       = aws_s3_bucket.this.arn
  description = "ARN of the created bucket."
}
```

## References

- Terraform Standard Module Structure: https://developer.hashicorp.com/terraform/language/modules/develop/structure
- Terraform Input Variables: https://developer.hashicorp.com/terraform/language/values/variables
- Terraform Output Values: https://developer.hashicorp.com/terraform/language/values/outputs
- Terraform Provider Versions: https://developer.hashicorp.com/terraform/language/providers/requirements
