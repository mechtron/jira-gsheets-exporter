terraform {
  required_version = ">= 0.12"
  # The configuration for this backend will be filled in by Terragrunt
  backend "s3" {
  }
}

provider "aws" {
  region = var.aws_region
}
