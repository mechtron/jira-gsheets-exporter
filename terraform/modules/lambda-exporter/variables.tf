variable "aws_region" {
  description = "The AWS region"
}

variable "environment" {
  description = "The service's environment"
}

variable "function_name" {
  description = "The Lambda function's name"
  default     = "jira-gsheets-exporter"
}

variable "repo_root_path" {
  description = "The hard path of this repository"
}

variable "google_service_creds_json" {
  description = "Google service account credentials (JSON string)"
}

variable "jira_api_email" {
  description = "The email associated with the Jira API token"
}

variable "jira_api_token" {
  description = "Jira API token"
}

variable "ses_from_email" {
  description = "The from: email address to send email alerts to"
}
