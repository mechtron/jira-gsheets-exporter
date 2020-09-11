FROM hashicorp/terraform:light
LABEL mechtron <mechtrondev@gmail.com>

ENV TERRAFORM_VERSION=0.12.17
ENV TERRAGRUNT_VERSION=0.21.6

RUN apk -v --update add go python3 py-pip alpine-sdk coreutils
RUN pip install --upgrade awscli

ADD https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip /
RUN unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

ADD https://github.com/gruntwork-io/terragrunt/releases/download/v$TERRAGRUNT_VERSION/terragrunt_linux_386 /bin/terragrunt
RUN chmod +x /bin/terragrunt

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
