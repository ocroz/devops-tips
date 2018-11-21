# Kubernetes cluster on openstack

References:
- http://superuser.openstack.org/articles/deploy-kubernetes-openstack-ansible/
- https://help.switch.ch/engines/documentation/configure-your-network/
- https://kubernetes.io/docs/setup/independent/install-kubeadm/

```bash
# Install kubeadm
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat <<EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
sudo apt-get update && sudo apt-get install -y kubeadm
# Install ansible
sudo apt install -y ansible
# Download ansible-playbook for kubernetes on openstack
git clone https://github.com/infraly/k8s-on-openstack
cd k8s-on-openstack
# Configure ansible-playbook for openstack tenant
vi config.sh
```

```bash
# https://github.com/infraly/k8s-on-openstack
# http://superuser.openstack.org/articles/deploy-kubernetes-openstack-ansible/
export OS_AUTH_URL=https://cloud.eu-zrh.hub.kudelski.com:5000/
export OS_DOMAIN_NAME=hq.k.grp
export OS_USERNAME=olivier.crozier@nagra.com
#export OS_PASSWORD=
export OS_PROJECT_NAME=cas-cmadmin-dev
export OS_PROJECT_ID=10aae9a5a1e2439e893b2c96702b9fc2
#export OS_REGION_NAME=ZH
export KEY=crozier-MOB100326

export NAME=k8s-cluster
export IMAGE=ubuntu-16.04-x86_64
export NETWORK=k.grp
export EXTERNAL_NETWORK=k.grp
export FLOATING_IP_POOL=private
export FLOATING_IP_NETWORK_UUID=b75b0790-fd14-4c05-822c-2c5287719f7a
export SUBNET_UUID=80361549-5e3a-41cf-a0b8-1d2482d4a48f
export NODE_FLAVOR=t2.small
#export NODE_COUNT=3
export NODE_AUTO_IP=True
#export NODE_DELETE_FIP=True
#export MASTER_BOOT_FROM_VOLUME=True
#export MASTER_TERMINATE_VOLUME=True
#export MASTER_VOLUME_SIZE=20GB
export MASTER_FLAVOR=t2.small
```

```bash
openstack server create --image "ubuntu-16.04-x86_64" --flavor "t2.small" --key-name "crozier-MOB100326" --security-group "ssh" --nic net-id="private" "k8s-cluster-master" # +node01 +node02 +node03
sudo vi /etc/hosts # Add the 4 above k8s machines with their floating IPs
ssh-keygen # without passphrase
```

On every new created k8s machine:
```bash
vi .ssh/authorized_keys # Add ubuntu@openstack:/home/ubuntu/.ssh/id_rsa.pub
sudo vi /etc/hosts # Add the 4 k8s machines with current machine as localhost
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python
which python
```

```bash
pip install shade && pip show shade
ansible all -i 'k8s-cluster-master,k8s-cluster-node01,k8s-cluster-node02,k8s-cluster-node03,' -m setup
sudo vi /etc/ansible/hosts
```

```bash
[all]
localhost ansible_connection=local ansible_python_interpreter="/usr/bin/env python"

[master]
k8s-cluster-master ansible_connection=ssh

[nodes]
k8s-cluster-node[01:03] ansible_connection=ssh

[all:children]
master
nodes
```

```bash
# Spin up a new cluster:
ansible-playbook site.yaml -i /etc/ansible/hosts
# Destroy the cluster:
ansible-playbook destroy.yaml
```

Cleaning:
```bash
pip uninstall shade
sudo apt --purge autoremove -y ansible kubeadm
```
