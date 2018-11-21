# Install docker on CentOS 7

## Docker itself

```bash
sudo yum update -y

# Either
sudo yum install docker -y

# Or
sudo yum install yum-utils device-mapper-persistent-data lvm2 -y
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce -y

# Version 18+
docker --version

sudo systemctl start docker
sudo systemctl status docker
sudo systemctl enable docker

sudo groupadd docker
sudo usermod -aG docker centos
sudo reboot

docker version
```

## Docker registry

## Docker example with nginx
