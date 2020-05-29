# Docker installation

## CentOS 7

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

## CentOS 8

```bash
sudo curl https://download.docker.com/linux/centos/docker-ce.repo \
          -o /etc/yum.repos.d/docker-ce.repo
sudo yum makecache
sudo yum install -y docker-ce --nobest # yum or dnf

# Version 18+
docker --version

sudo systemctl enable --now docker
sudo systemctl status docker

sudo usermod -aG docker centos # Then ssh logout, and re-login
docker version
```

# Docker additional features

## Docker mirror

References:
- https://stackoverflow.com/questions/28557384/docker-private-registry-with-mirror
- https://hackernoon.com/mirror-cache-dockerhub-locally-for-speed-f4eebd21a5ca
- https://docs.docker.com/registry/recipes/mirror/#run-a-registry-as-a-pull-through-cache

```bash
docker run -d -p 5000:5000 --restart=always --name registry -v /local/path/to/registry:/registry -e SETTINGS_FLAVOR=local -e STORAGE_PATH=/registry registry

docker run -d -p 5555:5000 --restart=always --name mirror -v /local/path/to/mirror:/registry -e STORAGE_PATH=/registry -e STANDALONE=false -e MIRROR_SOURCE=https:/registry-1.docker.io -e MIRROR_SOURCE_INDEX=https://index.docker.io registry

sudo vi /etc/docker/daemon.json
{
  "insecure-registries": ["http://localhost:5000"],
  "registry-mirrors": ["http://localhost:5555"],
  "metrics-addr" : "0.0.0.0:50501",
  "experimental" : true
}
sudo systemctl restart docker
```

## Docker registry

```bash
# Create the registry
docker run -d -p 5000:5000 --restart=always --name registry registry:2

# Pull an image, tag it, and push it to the local registry
docker pull alpine:latest
docker tag alpine:latest localhost:5000/alpine:latest
docker push localhost:5000/alpine:latest

# Remove the image, and pull it from the local registry
docker image rm alpine:latest localhost:5000/alpine:latest
docker pull localhost:5000/alpine:latest

# List the images in the registry
#docker pull distribution/registry:master
curl -I localhost:5000
curl http://localhost:5000/v2/_catalog
curl http://localhost:5000/v2/${repo}/tags/list # ex repo=alpine

# Stop the registry
docker container stop registry
```

## Docker example with nginx

Simple example +
See also Automated Nginx Reverse Proxy for Docker

```bash
# Dockerfile
FROM nginx
COPY conf.d/*.conf /etc/nginx/conf.d/

# Create and Run the image
docker build -t nginx-on-app:v1 .
docker create nginx-on-app:v1
docker run -p 8080:80 -td nginx-on-app:v1 # nginx:80->container:8080
```

## Bash into docker container

```bash
docker exec -it [CONTAINER_ID] bash
```

## Docker compose

## Docker service
