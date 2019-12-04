provider "credstash" {
  table  = var.credstash_table
  region = var.aws_region
}

data "credstash_secret" "google_creds_json" {
  name = "google_creds_json"
}

data "credstash_secret" "jira_api_token" {
  name = "jira_api_token"
}

data "credstash_secret" "jira_api_email" {
  name = "jira_api_email"
}
