variable "aws_region" {
  description = "The AWS region"
}

variable "credstash_table" {
  description = "Credstash DynamoDB table name"
}

variable "environment" {
  description = "The service's environment"
}

variable "function_name" {
  description = "The Lambda function's name"
  default     = "jira-gsheets-exporter"
}

variable "google_sheet_name" {
  description = "Name of the Google Sheet"
}

variable "google_sheet_tab_name" {
  description = "Name of the Google Sheet tab to sync Jira data to"
}

variable "jira_api_base_url" {
  description = "The base URL of the target Jira API"
}

variable "jira_max_issues_to_fetch" {
  description = "The max number of Jira issues to fetch"
  default     = 1000
}

variable "jira_project_name" {
  description = "The project key of the Jira project to fetch issues for"
}

variable "repo_root_path" {
  description = "The hard path of this repository"
}

variable "ses_from_email" {
  description = "The from: email address to send email alerts to"
}
