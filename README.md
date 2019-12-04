# jira-gsheets-exporter

By Corey Gale (`mechtrondev[at]gmail.com`)

## Executive summary

Exports data for a particular Jira project to a Google Sheet for further analysis. Includes Terraform IaC to provision an AWS Lambda function that runs every hour to keep your Google Sheet data up-to-date.

## Features

1. Scalable: can easily process Jira projects with large issue counts (10k+)
1. Updates Google Sheets very quickly (single API call)
1. Includes AWS Lambda function with hourly CloudWatch Events trigger
1. (coming soon) Email notifications via SES for failed executions

## AWS infrastructure

#### Resources

- Lambda function triggered by CloudWatch Events (fires hourly)
- CloudWatch Log Stream for Lambda function output

#### Estimated cost

All of the AWS resources provisioned by this project fit within [AWS's always-free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=tier%23always-free). Just to be safe, I suggest that you set up a [billing alarm](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html) for your AWS account to avoid any bill shock.

## Deploying `jira-gsheets-exporter` to your AWS account

### Dependencies

1. `make`
1. Terraform v0.12.x
1. Terragrunt v0.21.x
1. [`credstash`](https://github.com/fugue/credstash)

### Setup credentials

1. Obtain Google OAuth2 credentials:
	1. Open the [Google Developers Console](https://console.developers.google.com/project), select your organization and create a new project/select an existing one.
	1. Click the hamburger menu on the left > APIs & Services > Library
	1. Enable the Google Sheets and Google Drive APIs
	1. Click the back arrow and then the "Credentials" link on the left menu
	1. Click Create credentials > Service account key > New service account. Give your service account a name, make sure "JSON" is selected and click "Create". A JSON file will be automatically downloaded whose contents is your Google service account.

1. Obtain a Jira API token:
	1. Log in to the [Atlassian API tokens portal](https://id.atlassian.com/manage/api-tokens)
	1. Click "Create API token"
	1. From the dialog that appears, enter a memorable label for your token and click "Create"
	1. Click "Copy to clipboard" and paste the token elsewhere for reference later

1. Install the [`credstash`](https://github.com/fugue/credstash#setting-up-credstash) CLI and setup a new credstash table named `credstash`: `credstash -t credstash setup`. If you wish to use another table name, be sure to update the `credstash_table` value in `terraform/terragrunt/prod/terragrunt.hcl`.

1. Populate the following credstash secrets:
	1. `google_creds_json`: `credstash -t credstash put google_creds_json <your-google-service-account-json>`
	1. `jira_api_email`: `credstash -t credstash put jira_api_email <your-jira-email>`
	1. `jira_api_token`: `credstash -t credstash put jira_api_token <your-jira-token>`

### Deploy

1. Update the shared Terragrunt values in `terraform/terragrunt/terragrunt.hcl` to match your AWS account's configuration.
1. Open/create the target Google Sheets spreadsheet and share it with the email contained in the Google auth JSON (under `client_email`). Make sure the user has "Can edit" permissions.
1. Update the `prod` environment's Terragrunt values in `terraform/terragrunt/prod/terragrunt.hcl`:
	1. `google_sheet_name` is the name of the Google Sheet from the previous step
	1. `google_sheet_tab_name` is the name of the tab/worksheet within the Google sheet to sync data to
	1. `jira_project_name` is the project key of the Jira project to fetch issues for
1. Open `exporter/exporter.py` and update the Python mapping logic within `update_jira_data()`
1. Deploy the `prod` environment (using the Terragrunt variables stored in `terraform/terragrunt/prod/terragrunt.hcl`):

		ENV=prod TF_ACTION=apply make terragrunt

### Destroy

To destroy an environment (in this case `prod`), set the `TF_ACTION` environment variable to `destroy`:

	ENV=prod TF_ACTION=destroy make terragrunt

### Creating new environments

Creating new environments is as easy as creating a new Terragrunt environment folder:

1. Copy `terraform/terragrunt/prod/terragrunt.hcl` to a new sub-directory under `terraform/terragrunt/`. The name that you choose for this directory will be your new environment's name.
1. Update the environment's name in the newly copied `terragrunt.hcl` file under the `inputs` section near the end of the file.
1. Deploy your environment with `make`:

		ENV=<ENV> TF_ACTION=apply make terragrunt

	Where `<ENV>` is your new environment's name

## To do

1. Send failure notifications via SES
1. Add GitHub Actions deployment pipeline
