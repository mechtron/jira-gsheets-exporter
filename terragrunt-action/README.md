# terragrunt-action

This action executes Terraform via Terragrunt and stores module exports as GitHub Action outputs.

## Inputs

### `env`

**Required** The name of the Terragrunt environment

### `tf_action`

**Required** Terraform `apply` or `destroy`?

## Outputs

### `function_arn`

The Lambda function's ARN

### `source_code_hash`

The Lambda-generated hash of the function's source code

### `last_modified`

The Lambda function's source code last modified date

## Example usage

```
uses: mechtron/jira-gsheets-exporter/terragrunt-action@2.0.0
with:
  env: prod
  tf_action: apply
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```
