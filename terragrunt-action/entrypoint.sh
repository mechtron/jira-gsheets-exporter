#!/bin/sh -l

pip install -r $GITHUB_WORKSPACE/exporter/requirements.txt -t exporter

aws sts get-caller-identity
aws s3 ls

export TF_VAR_repo_root_path=$GITHUB_WORKSPACE/ && \
	cp $GITHUB_WORKSPACE/config/$1.yml $GITHUB_WORKSPACE/exporter/config.yml && \
	cd $GITHUB_WORKSPACE/terraform/terragrunt/$1 && \
	terragrunt $2 --terragrunt-source-update --auto-approve=true
