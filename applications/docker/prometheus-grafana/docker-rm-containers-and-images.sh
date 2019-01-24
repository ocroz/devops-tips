#!/usr/bin/bash

# Remove running containers
contids=$(docker ps | grep psmonitoring | cut -d' ' -f1)
for contid in $contids; do docker stop $contid; docker rm $contid; done

# Remove other containers
contids=$(docker ps --all | grep -E "psmonitoring|alpine" | cut -d' ' -f1)
for contid in $contids; do docker rm $contid; done

# Remove images
imgids=$(docker images | grep -E "psmonitoring|alpine" | sed 's,  *, ,g' | cut -d' ' -f3)
for imgid in $imgids; do docker image rm $imgid; done
