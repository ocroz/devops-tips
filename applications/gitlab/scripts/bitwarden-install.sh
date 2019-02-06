# Install docker-compose
DC_VERSION="1.23.2"
sudo curl -L "https://github.com/docker/compose/releases/download/${DC_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Download installer
curl -s -o bitwarden.sh \
    https://raw.githubusercontent.com/bitwarden/core/master/scripts/bitwarden.sh \
    && chmod +x bitwarden.sh

# Interractive installer
./bitwarden.sh install
