FROM ubuntu:18.04

# Install basic packages
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    jq \
    python3 \
    bash \
    git \
    openssl \
    python3-pip \
    python-pip \
    gnupg2 \
    libssl-dev \
    iputils-ping \
    apt-transport-https \
    ca-certificates \
    gnupg-agent \
    software-properties-common

# add apt repos
# add gcloud repo
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
# add docker repo
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
# add ansible repo
RUN apt-add-repository --yes --update ppa:ansible/ansible

# variables
ENV PACKER_VERSION=1.5.4
ENV TERRAFORM_VERSION=0.12.8

# Install packages
RUN apt-get update && apt-get install -y \
    google-cloud-sdk \
    ansible \
    docker-ce \
    docker-ce-cli \
    containerd.io

# Packer Installation
RUN wget https://releases.hashicorp.com/packer/${PACKER_VERSION}/packer_${PACKER_VERSION}_linux_amd64.zip && \
    unzip packer_${PACKER_VERSION}_linux_amd64.zip -d /usr/local/bin/
RUN rm packer_${PACKER_VERSION}_linux_amd64.zip

# Terraform Installation
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
    unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin/
RUN rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Molecule installation
RUN pip install 'molecule[docker]'
