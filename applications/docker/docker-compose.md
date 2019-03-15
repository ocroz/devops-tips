# Install docker-compose

## Installation

```bash
DC_VERSION="1.23.2"
sudo curl -L "https://github.com/docker/compose/releases/download/${DC_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

docker-compose version
```

## Usage
