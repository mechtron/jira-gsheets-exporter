#!/bin/sh -l

pip install -r $GITHUB_WORKSPACE/exporter/requirements.txt -t $GITHUB_WORKSPACE/exporter/

export TF_VAR_repo_root_path=$GITHUB_WORKSPACE
export TF_VAR_google_service_creds_json=$GOOGLE_SERVICE_CREDS_JSON
export TF_VAR_jira_api_email=$JIRA_API_EMAIL
export TF_VAR_jira_api_token=$JIRA_API_TOKEN
cp $GITHUB_WORKSPACE/config/$1.yml $GITHUB_WORKSPACE/exporter/config.yml
cd $GITHUB_WORKSPACE/terraform/terragrunt/$1
terragrunt $2 --terragrunt-source-update --auto-approve=true
