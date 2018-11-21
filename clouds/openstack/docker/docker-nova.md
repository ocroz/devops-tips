# Docker on openstack

References:
- https://wiki.openstack.org/wiki/Docker

```bash
sudo apt-get --purge autoremove -y docker docker-engine docker.io
sudo rm -rf /usr/local/bin/docker-machine*

sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable"
sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install -y docker-ce

apt-cache madison docker-ce
sudo docker run hello-world

pip install -e git+https://github.com/stackforge/nova-docker#egg=novadocker
cd ~/openstack/src/novadocker/ && \
  git checkout HEAD^1 && \
  python setup.py install

sudo mkdir /etc/nova && sudo vi /etc/nova/nova.conf
sudo mkdir /etc/nova/rootwrap.d && sudo vi /etc/nova/rootwrap.d/docker.filters

glance image-list
# The request you have made requires authentication. (HTTP 401)

sudo docker search hipache
sudo docker pull hipache
sudo docker save hipache | glance image-create --container-format=docker --disk-format=raw --name hipache
# The request you have made requires authentication. (HTTP 401)

sudo docker pull busybox
sudo docker save busybox | openstack image create busybox --public --container-format docker --disk-format raw
# The request you have made requires authentication. (HTTP 401)
```
