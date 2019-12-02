# jira-sprint-analyzer

By Corey Gale (`mechtrondev[at]gmail.com`)

## Executive summary

Syncs data for a particular Jira project to a Google Sheet for further analysis. Includes Terraform IaC to provision a AWS Lambda function that runs nightly to always keep your Google Sheet data up-to-date.

## Features

1. Can anaylze a large number of Jira issues (10k+)
1. Updates Goolge Sheets very quickly (single API call)
1. Includes AWS Lambda function with nightly triggers
1. (coming soon) Email notifications via SES for failed executions

## AWS infrastructure

#### Resources

- Lambda function triggered by CloudWatch Events (fires nightly at UTC midnight)
- CloudWatch Log Stream for Lambda function output
- SES for email notifications

#### Estimated cost

All of the AWS resources provisioned by this project fit within [AWS's always-free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free).

Just to be safe, to avoid bill shock I suggest that you set up a [billing alarm](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html) for your AWS account.

## Deploying `jira-sprint-analyzer` to your AWS account

#### Dependencies

1. `make`
1. Terraform v0.12.x
1. Terragrunt v0.20.x

#### Deploy an environment

1. Update the Terragrunt values in `terraform/terragrunt/terragrunt.hcl` to match your AWS account's configuration.
1. To deploy the `prod` environment (using the Terragrunt variables stored in `terraform/terragrunt/prod/terragrunt.hcl`):

		ENV=prod TF_ACTION=apply make terragrunt

#### Destroy an environment

To destroy an environment (in this case `prod`), set the `TF_ACTION` environment variable to `destroy`:

	ENV=prod TF_ACTION=destroy make terragrunt

#### Creating new environments

Creating new environments is as easy as creating a new Terragrunt environment folder:

1. Copy `terraform/terragrunt/prod/terragrunt.hcl` to a new sub-directory under `terraform/terragrunt/`. The name that you choose for this directory will be your new environment's name.
1. Update the environment's name in the newly copied `terragrunt.hcl` file under the `inputs` section near the end of the file.
1. Deploy your environment with `make`:

		ENV=<ENV> TF_ACTION=apply make terragrunt

	Where `<ENV>` is your new environment's name.

## To do

1. Send failure notifications via SES
1. Add infrastructure diagram
1. Add GitHub Actions deployment pipeline
