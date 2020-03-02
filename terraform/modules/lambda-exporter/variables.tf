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

variable "repo_root_path" {
  description = "The hard path of this repository"
}

variable "ses_from_email" {
  description = "The from: email address to send email alerts to"
}
