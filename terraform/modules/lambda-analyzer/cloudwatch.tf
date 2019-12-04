resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda_function.function_name}"
  retention_in_days = 3
}

resource "aws_cloudwatch_event_rule" "lambda_function_trigger" {
  name                = "${var.function_name}-${var.environment}-trigger"
  schedule_expression = "rate(1 hour)"
  depends_on          = [aws_lambda_function.lambda_function]
}

resource "aws_cloudwatch_event_target" "lambda_function_trigger_target" {
  target_id = aws_cloudwatch_event_rule.lambda_function_trigger.name
  rule      = aws_cloudwatch_event_rule.lambda_function_trigger.name
  arn       = aws_lambda_function.lambda_function.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call" {
  function_name = aws_lambda_function.lambda_function.function_name
  source_arn    = aws_cloudwatch_event_rule.lambda_function_trigger.arn
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  statement_id  = "AllowExecutionFromCloudWatch"
}
