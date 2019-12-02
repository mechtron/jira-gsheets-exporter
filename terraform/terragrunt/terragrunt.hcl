remote_state {
  backend = "s3"
  config = {
    bucket  = "gumgum-terraform-state"
    key     = "jira-sprint-analyzer/${path_relative_to_include()}/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true

    # Tell Terraform to do locking using DynamoDB. Terragrunt will automatically
    # create this table for you if it doesn't already exist.
    lock_table = "terraform-lock-table"
  }
}

terraform {
  # Force Terraform to keep trying to acquire a lock for up to 20 minutes
  # if someone else already has the lock.
  extra_arguments "retry_lock" {
    commands = [
      "init",
      "apply",
      "refresh",
      "import",
      "plan",
      "taint",
      "untaint"
    ]

    arguments = [
      "-lock-timeout=20m"
    ]
  }
}

inputs = {
  aws_region = "us-east-1"
  credstash_table = "va-credstash-jira-sprint-analyzer"
}
