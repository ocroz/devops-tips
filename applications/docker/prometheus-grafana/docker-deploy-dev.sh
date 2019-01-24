#!/usr/bin/bash

# Set variable for prometheus
export DOCKER_HOST_IP=$(hostname -I | cut -d' ' -f1)

# Run docker compose
docker-compose -f docker-compose.yml -f docker-compose-dev-lnx.yml up -d

# Exit here if no need for a reverse proxy in front
exit 0

# Restart running containers with a VIRTUAL_HOST environment
contids=$(docker ps | grep -E "/prometheus|/grafana" | cut -d' ' -f1)
for contid in $contids; do docker stop $contid; done
docker run -e VIRTUAL_HOST=prometheus -p 9090:9090 -td psmonitoring/prometheus:v2.3.1
docker run -e VIRTUAL_HOST=grafana -p 3000:3000 -td psmonitoring/grafana:5.2.1
