#!/bin/sh -l

set -e

# Copy app environment config.yml
cp $GITHUB_WORKSPACE/config/$1.yml $GITHUB_WORKSPACE/exporter/config.yml

# Set Terraform input vars
export TF_VAR_repo_root_path=$GITHUB_WORKSPACE
export TF_VAR_google_service_creds_json=$GOOGLE_SERVICE_CREDS_JSON
export TF_VAR_jira_api_email=$JIRA_API_EMAIL
export TF_VAR_jira_api_token=$JIRA_API_TOKEN

# Run Terragrunt
cd $GITHUB_WORKSPACE/terraform/terragrunt/$1
terragrunt $2 --terragrunt-source-update --auto-approve=true

# Conditionally set Terragrunt exports as Action outputs
if [[ $2 = "destroy" ]]
then
    echo "Stack destroyed - no output variables to print"
else
    # Grab Terraform export vars
    export FUNCTION_ARN=`terragrunt output lambda_arn`
    export SOURCE_CODE_HASH=`terragrunt output lambda_source_code_hash`
    export LAST_MODIFIED=`terragrunt output lambda_last_modified`

    # Set Action output vars
    echo ::set-output name=function_arn::$FUNCTION_ARN
    echo ::set-output name=source_code_hash::$SOURCE_CODE_HASH
    echo ::set-output name=last_modified::$LAST_MODIFIED
fi
