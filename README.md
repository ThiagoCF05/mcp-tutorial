# mcp-tutorial
Step-by-step tutorial on how to generate an MCP server

Start an 't4g.xlarge' instance

```bash
sudo apt -y update
sudo apt -y upgrade
sudo apt-get install  curl apt-transport-https ca-certificates software-properties-common
sudo snap install yq
```

## Install Docker

```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## Install Git

```
sudo apt install git
```

## Install Python

```
sudo apt -y install python3-pip
```

## Build Image

```
git clone https://github.com/ThiagoCF05/mcp-tutorial.git
cd mcp-tutorial
docker build -t mcp-server .
docker run -d -p 8080:8080 mcp-server
```

## Step 1: Download the eksctl CLI tool

```
curl "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_arm64.tar.gz" \
    --silent --location \
    | tar xz -C /tmp
sudo install -m 0755 /tmp/eksctl /usr/local/bin/eksctl
```

```
# Source https://github.com/eksctl-io/eksctl
# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=arm64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /tmp && rm eksctl_$PLATFORM.tar.gz

sudo install -m 0755 /tmp/eksctl /usr/local/bin && rm /tmp/eksctl
```

## Step 2: Install the Amazon EKS Anywhere plugin

```
curl https://anywhere-assets.eks.amazonaws.com/releases/eks-a/99/artifacts/eks-a/v0.22.5/linux/arm64/eksctl-anywhere-v0.22.5-linux-arm64.tar.gz \
    --silent --location \
    | tar xz ./eksctl-anywhere
sudo install -m 0755 ./eksctl-anywhere /usr/local/bin/eksctl-anywhere
```

```
cd ~

export EKSA_RELEASE="0.9.1" OS="$(uname -s | tr A-Z a-z)" RELEASE_NUMBER=12


curl "https://anywhere-assets.eks.amazonaws.com/releases/eks-a/${RELEASE_NUMBER}/artifacts/eks-a/v${EKSA_RELEASE}/${OS}/arm64/eksctl-anywhere-v${EKSA_RELEASE}-${OS}-arm64.tar.gz" --silent --location | tar xz ./eksctl-anywhere

sudo mv ./eksctl-anywhere /usr/local/bin/ 

cd /usr/local/bin
ls
```

## Step 3: Install kubectl

```
cd ~
export OS="$(uname -s | tr A-Z a-z)" ARCH=$(test "$(uname -m)" = 'x86_64' && echo 'amd64' || echo 'arm64')
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/${OS}/${ARCH}/kubectl"
sudo install -m 0755 ./kubectl /usr/local/bin/kubectl
```


## Step 4: Define Cluster Configuration

```
cd ~
CLUSTER_NAME=dev-cluster
eksctl anywhere generate clusterconfig $CLUSTER_NAME --provider docker > $CLUSTER_NAME.yaml
```

## Step 5: Create the Cluster

```
CLUSTER_NAME=dev-cluster
sudo eksctl anywhere create cluster -f $CLUSTER_NAME.yaml
```

