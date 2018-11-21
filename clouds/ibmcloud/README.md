# DevOps with `docker` and `kubernetes` on the IBM Cloud

## Table of Contents
1. [Installation](#installation)
2. [Docker](#docker)
3. [Kubernetes](#kubernetes)

## References

- https://console.bluemix.net/
- https://www.ibm.com/developerworks/cloud/library/cl-getting-started-docker-and-kubernetes/index.html
-- https://www.youtube.com/watch?v=vLMX9gyTEr4
-- https://www.youtube.com/watch?v=EOxQS4ROiOw

## Installation

### On Windows 10 Pro

- IBM Cloud tools AND plugins.
- Docker for Windows +Kitematic.
- Note: Docker uses Hyper-V from the Windows distribution.
- Kubernetes (might be installed via docker).

### On Windows 10 Home

- IBM Cloud tools AND plugins.
- Docker Toolbox for Windows (inc. Kitematic).
- VirtualBox (might be installed via docker).
- Kubernetes.

## Docker

### Create a docker container

Create a `Dockerfile` (or `git clone https://github.com/IBM/dWTVSimpleContainerApp`):

```
FROM ibmcom/ibmnode:latest

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY package.json /usr/src/app
RUN npm install

EXPOSE 6006

COPY . /usr/src/app

CMD ["node", "app.js"]
```

Run the docker commands:

```bash
docker version|info              # Docker is installed
docker run hello-world        # Execute a docker image
docker build -t basicapp:v1 .   # Build a docker image
docker create basicapp:v1         # Create a container
docker image ls                      # List the images
docker container ls | docker ps  # List the containers
```

### SSH to server and container

On Windows the VM disks are saved into:
- Hyper-V: C:\Users\Public\Documents\Hyper-V\Virtual hard disks\MobyLinuxVM.vhdx
- VirtualBox: C:\Users\Denise\\\.docker\machine\machines\default\disk.vmdk

Log into the underlying VM and look at the containers and images:

```text
docker run -it --rm --privileged --pid=host justincormack/nsenter1
# ls /var/lib/docker/containers/
# cat /var/lib/docker/image/overlay2/repositories.json
# exit
```

Log into the container:

```text
docker exec -it [CONTAINER_ID] bash
# ps aux
# which node
# exit
```

Debug the container if it fails to startup:

```text
docker commit [CONTAINER_ID] temporary_image
docker run --entrypoint=bash -it temporary_image
# ls
# exit
```

### Open the app in browser

Open `Kitematic`, select the appropriate `Container`, click on `Settings`, then `Hostname/Ports`, and `Configure Ports` with:

| DOCKER PORT | PUBLISHED IP:PORT |
| ---- | ---- |
| 6006 | localhost:32008 |

Command line alternative:
```bash
docker ps                                # Get the container id
docker inspect ${container-id} | grep IP # Get the container published ip
docker port ${container-id} 6006         # Get the container published port
```

Then open the app at http://localhost:32008/ or http://vboxlocal:32008/.

## Kubernetes

Create the kubernetes cluster at the IBM Cloud, then...

Login to your IBM Cloud, and install the plusgins.

```bash
bx login -a https://api.eu-de.bluemix.net
bx plugin install container-service -r Bluemix
bx plugin install container-registry -r Bluemix
```

Connect `kubectl` to your IBM Cloud.

```bash
bx cs region-set eu-central
bx cs cluster-config mycluster # Name of the cluster
export KUBECONFIG=$HOME/.bluemix/.../mycluster/kube-config-mil01-mycluster.yml
kubectl get nodes
```

Create an image in your IBM Cloud with either:

```bash
bx cr login
bx cr namespace-add mybag # Name of the namespace
bx cr build -t registry.eu-de.bluemix.net/mybag/basicapp:v1 . # Change URL, namespace, image, tag
bx cr images
```

Or:

```bash
docker tag basicapp:v1 registry.eu-de.bluemix.net/mybag/basicapp:v2
docker push registry.eu-de.bluemix.net/mybag/basicapp:v2
```

Create the container and expose it to the world.

```bash
kubectl run apptest --image=registry.eu-de.bluemix.net/mybag/basicapp:v1
kubectl expose deployment/apptest --type=NodePort --name=apptest-service --port=6006
kubectl describe service apptest-service  # Get NodePort
bx cs workers mycluster                  # Get public IP
```
