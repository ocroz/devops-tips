# Training

O'Reilly Safari
30 days trial code UTSWK19

# Docker

An image is just a tar file.

```bash
# runs in detach mode to give the shell back before the command terminates
docker run -d $image $command

# pull then run
docker pull redis
docker run -d redis
```

We can share namespaces between containers:
- process tree
- network stack
- hostname
(there are 6-7 namespaces in Linux)

Kernel:
- namespace
- cgroup
-> LXC (Linux Containers)
-> Docker (UX on LXC)

LXC now LXD (daemon) which looks like a VM at using (ssh into container).
In parallel LXC has now different container runtimes like containerd.
And on Linux side `systemd-nspawn` is an alternative to LXC.

```bash
docker search $string # architecture dependent (arm, ppc, etc.)
```

Push to https://hub.docker.com/
In Artifactory, the tags are immutable, not in dockerhub.

With Scala there are docker plugins that create the the Dockerfile.

Official centos image  FROM scratch with ADD
```bash
FROM scratch
ADD centos-8-container.tar.xz /

LABEL org.label-schema.schema-version="1.0" \
    org.label-schema.name="CentOS Base Image" \
    org.label-schema.vendor="CentOS" \
    org.label-schema.license="GPLv2" \
    org.label-schema.build-date="20190927"

CMD ["/bin/bash"]
```

Linux namespaces:
```bash
# Network
docker run --net=null -d busybox sleep 3600
docker run -d busybox sleep 3600
docker run --net=$net -d busybox sleep 3600
docker run --net=host -d busybox sleep 3600
docker run --net=container:ID -d busybox sleep 3600

# Processes
docker run -d busybox sleep 3600
docker run --pid=host -d busybox sleep 3600
docker run --pid=container:ID -d busybox sleep 3600
```

`podman` runs in the user namespace when `docker` runs in the root namespace.
<br/>Both have the same interface.

podman cannot expose to a priviledge post as a user:
```bash
podman run -d -p 80:80 nginx # Fails
podman run -d -p 8080:80 nginx # Works
```

Attack: tcp dump of a network interface.
ln /var/log/xxx/0.log -> /etc/shadow
