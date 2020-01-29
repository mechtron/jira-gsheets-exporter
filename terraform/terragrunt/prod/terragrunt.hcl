# Terragrunt will copy the Terraform configurations specified by the source parameter, along with any files in the
# working directory, into a temporary folder, and execute your Terraform commands in that folder.
terraform {
  source = "../../modules//lambda-exporter"
}

# Include all settings from the root terragrunt.hcl file
include {
  path = find_in_parent_folders()
}

# These are the variables we have to pass in to use the module specified in the terragrunt configuration above
inputs = {
  environment = "prod"
  google_sheet_name = "DevOps Team Sprint Analyzer"
  google_sheet_tab_name = "Data"
  jira_project_name = "OPS"
  jira_max_issues_to_fetch = 1500
  ses_from_email = "mechtrondev@gmail.com"
}
