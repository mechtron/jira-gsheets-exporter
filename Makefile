TF_ACTION?=apply

pip:
	pip3 install -r exporter/requirements.txt -t exporter

terragrunt: pip
	export TF_VAR_repo_root_path=$(shell pwd) && \
	cp config/$(ENV).yml exporter/config.yml && \
	cd terraform/terragrunt/$(ENV) && \
	terragrunt $(TF_ACTION) --terragrunt-source-update --auto-approve=true
