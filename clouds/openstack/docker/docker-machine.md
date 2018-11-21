# Docker on openstack

References:
- https://www.objectif-libre.com/fr/blog/2015/11/09/integration-de-docker-dans-openstack/

```bash
sudo apt-get install -y docker-engine unzip

cd docker-machine
curl -L https://github.com/docker/machine/releases/download/v0.5.0/docker-machine_linux-amd64.zip >machine.zip
sudo unzip machine.zip -d /usr/local/bin/

export OS_TENANT_NAME=olivier.crozier@nagra.com
docker-machine --debug create -d openstack \
--openstack-ssh-user ubuntu \
--openstack-image-name ubuntu-14.04-x86_64 \
--openstack-flavor-name t2.small \
--openstack-net-name k.grp \
--openstack-floatingip-pool private \
--openstack-sec-groups ssh \
docker-machine
```
