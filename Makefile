TF_ACTION?=apply

pip:
	pip3 install -r analyzer/requirements.txt -t analyzer

terragrunt: pip
	export TF_VAR_repo_root_path=$(shell pwd) && \
	cd terraform/terragrunt/$(ENV) && \
	terragrunt $(TF_ACTION) --terragrunt-source-update --auto-approve=true
