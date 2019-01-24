# Collect metrics with prometheus + Metrics dashboard with grafana

## Install docker

See https://blogs.msdn.microsoft.com/premier_developer/2018/04/20/running-docker-windows-and-linux-containers-simultaneously/

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

## Install docker-compose

```bash
DC_VERSION="1.23.1"
sudo curl -L "https://github.com/docker/compose/releases/download/${DC_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

docker-compose version
```

## Prometheus

```bash
docker version # Server OS/Arch linux/amd64
docker container run --detach --publish-all prom/prometheus:v2.5.0
docker ps # localhost:port
```

powershell:
```bash
docker version # Server OS/Arch windows/amd64
docker container run --detach --publish-all dockersamples/aspnet-monitoring-prometheus:2.3.1
docker container run --platform=linux ... # with experimental features
docker ps # localhost:port
```

## Launch prometheus + grafana + few apps with docker-compose

First:
- Automated nginx reverse proxy for docker.
- Create a local dns server to map the names `host.docker.internal`, `prometheus`, and `java` to the docker machine IP (not 127.0.0.1).
- Turn the docker daemon metrics on (if you’re running the docker daemon as a systemd service).

To turn turn the docker daemon metrics on:
```bash
# /etc/docker/daemon.json
{
  "metrics-addr" : "0.0.0.0:50501",
  "experimental" : true
}

# Then restart docker
sudo systemctl restart docker
```

```bash
docker-compose -f docker-compose.yml -f docker-compose-dev-lnx.yml up -d

docker stop ${container-id-prometheus} ${contid-grafana} ${contid-java}
docker run -e VIRTUAL_HOST=prometheus -p 9090:9090 -td psmonitoring/prometheus:v2.3.1
docker run -e VIRTUAL_HOST=grafana -p 3000:3000 -td psmonitoring/grafana:5.2.1
docker run -e VIRTUAL_HOST=java -p 8080:8080 -td psmonitoring/java:v2
```

## Launch everything in a swarm cluster

```bash
# Open the firewall
sudo firewall-cmd --add-port=2376/tcp --permanent
sudo firewall-cmd --add-port=2377/tcp --permanent
sudo firewall-cmd --add-port=7946/tcp --permanent
sudo firewall-cmd --reload

# Create a docker swarm cluster
docker swarm init                  # From a swarm master
docker swarm join --token ${token} # From a swarm worker node
docker swarm leave                 # --force from a swarm master
docker node ls

# Add a docker config
docker-compose -f docker-compose.yml -f docker-compose-prod.yml config \
  | docker config create psmonitoring-prometheus -
docker config ls
docker config inspect --pretty psmonitoring-prometheus

# Start a docker service
docker stack deploy --compose-file docker-compose.yml --compose-file docker-compose-prod.yml stackpsmonitoring
docker stack ls
docker service ls
docker service ps ${service-name}
docker service inspect ${service-name}
docker stack rm stackpsmonitoring
```

Expose metrics from java app
```bash
#bash
docker image build -t psmonitoring/java:v1 -f ./docker/java/Dockerfile .
docker container run -d -P psmonitoring/java:v1
docker container ls --last 1

#powershell
docker image build -t psmonitoring/netfx:v1 -f .\docker\netfx\Dockerfile .
```

promql
```bash
sum(irate($metric[12h])) without (host, instance, job, exported_instance)
```

Standard metrics for any language such as java/scala, node.js, etc.

docker stack deploy creates or updates services as necessary.

Prometheus Metric and Label naming:
https://prometheus.io/docs/practices/naming/

Grafana community dashboards, or share/export then in Dockerfile
- COPY datasource-prometheus.yml
- COPY dashboard-provider.yml
- COPY ${your-dashboard}.json
