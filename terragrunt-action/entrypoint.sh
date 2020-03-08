#!/bin/sh -l

ls -laht /github/
ls -laht /github/home/
ls -laht /github/workflow/
ls -laht /github/workspace/

pip install -r /github/workspace/exporter/requirements.txt -t exporter

export TF_VAR_repo_root_path=/github/workspace/ && \
	cp /github/workspace/config/$1.yml /github/workspace/exporter/config.yml && \
	cd /github/workspace/terraform/terragrunt/$1 && \
	terragrunt $2 --terragrunt-source-update --auto-approve=true
