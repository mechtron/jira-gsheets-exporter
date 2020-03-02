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
  timeout          = "300"

  environment {
    variables = {
      GOOGLE_SERVICE_CREDS_JSON = data.credstash_secret.google_creds_json.value
      JIRA_API_EMAIL            = data.credstash_secret.jira_api_email.value
      JIRA_API_TOKEN            = data.credstash_secret.jira_api_token.value
    }
  }

  tags = {
    Name        = var.function_name
    Environment = var.environment
  }
}
