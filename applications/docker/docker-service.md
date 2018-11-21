# Run a docker service in a swarm cluster

## Create a swarm cluster

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
```

## Launch a service across all docker worker nodes

```bash
# Add a docker config
docker-compose -f docker-compose.yml -f docker-compose-prod.yml config \
  | docker config create psmonitoring-prometheus -
docker config ls
docker config inspect --pretty psmonitoring-prometheus

# Start a docker service
docker stack deploy --compose-file docker-compose.yml --compose-file docker-compose-prod.yml stackpsmonitoring
docker service ls
docker stack rm stackpsmonitoring
```
