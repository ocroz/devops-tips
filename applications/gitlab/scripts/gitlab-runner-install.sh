# https://docs.gitlab.com/runner/install/
# https://docs.gitlab.com/runner/install/linux-repository.html

# Install gitlab-runner
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh | sudo bash
sudo yum update -y
sudo yum install gitlab-runner -y

# Install docker too
sudo yum install yum-utils device-mapper-persistent-data lvm2 -y
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce -y

# Version 18+
docker --version

# Start and Enable docker
sudo systemctl start docker
sudo systemctl enable docker

# Make centos a docker user
sudo groupadd docker
sudo usermod -aG docker centos
sudo reboot
