output "lambda_arn" {
  value = "${aws_lambda_function.lambda_function.arn}"
}

output "lambda_source_code_hash" {
  value = "${aws_lambda_function.lambda_function.source_code_hash}"
}

output "lambda_last_modified" {
  value = "${aws_lambda_function.lambda_function.last_modified}"
}
