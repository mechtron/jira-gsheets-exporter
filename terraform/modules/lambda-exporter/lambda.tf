locals {
  zip_output_path = "jira-gsheets-exporter.zip"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${var.repo_root_path}/exporter/"
  output_path = local.zip_output_path
}

resource "aws_lambda_function" "lambda_function" {
  filename         = local.zip_output_path
  function_name    = "${var.function_name}-${var.environment}"
  role             = aws_iam_role.lambda_role.arn
  handler          = "exporter.handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.6"
  memory_size      = "512"
  timeout          = "180"

  environment {
    variables = {
      GOOGLE_SERVICE_CREDS_JSON = data.credstash_secret.google_creds_json.value
      GOOGLE_SHEET_NAME         = var.google_sheet_name
      GOOGLE_SHEET_TAB_NAME     = var.google_sheet_tab_name
      JIRA_API_EMAIL            = data.credstash_secret.jira_api_email.value
      JIRA_API_TOKEN            = data.credstash_secret.jira_api_token.value
      JIRA_API_BASE_URL         = var.jira_api_base_url
      JIRA_MAX_ISSUES_TO_FETCH  = var.jira_max_issues_to_fetch
      JIRA_PROJECT_NAME         = var.jira_project_name
    }
  }

  tags = {
    Name        = var.function_name
    Environment = var.environment
  }
}
