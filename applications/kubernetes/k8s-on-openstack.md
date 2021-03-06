# By Infraly

References:
- https://github.com/infraly/k8s-on-openstack
- https://superuser.openstack.org/articles/deploy-kubernetes-openstack-ansible
- https://stackoverflow.com/questions/18050911

## Authentication to Openstack

2 methods:
- Either define the environment variable `OS_CLOUD` with these files:
- Or DO NOT define the environment variable `OS_CLOUD`, but define other vars:

PUBLIC CLOUDS: /etc/openstack/clouds-public.yaml
```yaml
public-clouds:
  eu-zrh:
    auth:
      auth_url: https://cloud.eu-zrh.hub.kudelski.com:5000/
  us-phx:
    auth:
      auth_url: https://cloud.us-phx.hub.kudelski.com:5000/
```

OS CLOUDS: ~/.config/openstack/clouds.yaml (auth.password required for ansible)
```yaml
clouds:
  eu-zrh-cas-cmadmin-dev:
    profile: eu-zrh
    identity_api_version: '3'
    interface: public
    auth:
      domain_name: hq.k.grp
      project_name: cas-cmadmin-dev
      username: <email>
      password: <password>
```

OS VARS: ~/bin/openstack-password.sh (OS_PROJECT_ID required for k8s nginx)
```bash
# Either define this variable:
export OS_CLOUD=eu-zrh-cas-cmadmin-dev

# Or define these other variables:
export OS_AUTH_URL=https://cloud.eu-zrh.hub.kudelski.com:5000/
export OS_PROJECT_NAME=cas-cmadmin-dev
export OS_PROJECT_ID=10aae9a5a1e2439e893b2c96702b9fc2
export OS_DOMAIN_NAME=hq.k.grp
export OS_USERNAME=olivier.crozier@nagra.com

echo "Please enter your OpenStack Password: "
read -sr OS_PASSWORD_INPUT
export OS_PASSWORD=$OS_PASSWORD_INPUT
```

## Configuration of Kubernetes cluster

K8s settings: ~/bin/k8s-on-openstack-env.sh
```bash
export KEY=crozier-nagra

export NAME=k8s
export IMAGE=ubuntu-16.04-x86_64

export EXTERNAL_NETWORK=k.grp
export NETWORK=k8s
#export FLOATING_IP_POOL=
#export FLOATING_IP_NETWORK_UUID=

export NODE_FLAVOR=t2.micro

#export NODE_COUNT=3
#export NODE_AUTO_IP=false
#export NODE_DELETE_FIP=true
#export MASTER_BOOT_FROM_VOLUME=true
#export MASTER_TERMINATE_VOLUME=true

export MASTER_VOLUME_SIZE=16
export MASTER_FLAVOR=t2.micro

#export INCLUDE_HELM=false
#export HELM_REPOS=
#export HELM_INSTALL=
```

K8s inventory: ~/.config/openstack/k8s-hosts (Do NOT list localhost!)
```
[master]
k8s-master

[nodes]
k8s-node[01:03]

[all:children]
master
nodes

[all:vars]
ansible_connection=ssh
ansible_python_interpreter=/usr/bin/python3
```

Replace group_vars/all.yaml
```bash
-nodes_name: "{{ name }}-" # node id will automatically be appended
+nodes_name: "{{ name }}-node" # node id will automatically be appended
```

Replace roles/openstack-nodes/tasks/main.yaml (*n)
```bash
-      hostname: "{{ nodes_name }}{{ item }}"
+      hostname: "{{ nodes_name }}{{ '%02d'|format(item|int) }}"
```

## Run the ansible playbook

Either run the entire playbook straight forward, or go and fix the issues one by one when they happen.

Steps:
```bash
# Source the environment
source ~/bin/openstack-password.sh
source ~/bin/k8s-on-openstack-env.sh

# Create the network
grep -B500 openstack-security-groups site.yaml > site-network.yaml
ansible-playbook -i ~/.config/openstack/k8s-hosts site-network.yaml
rm site-network.yaml

# Export network variables
openstack token issue
export FLOATING_IP_NETWORK_UUID=$(openstack network show k8s -f value -c id)
export SUBNET_UUID=$(openstack subnet show k8s -f value -c id)

# Play the entire playbook
ansible-playbook -i ~/.config/openstack/k8s-hosts site.yaml

# If "Wait during instances boot" fails for k8s master,
# This is most probably due to ssh not started (manual ssh should fail too).
# Solution: Delete the newly created host and try again.

# If "Wait for cloud-init to finish" fails for k8s master or nodes,
# Increase values in roles/common/tasks/main.yaml
-  retries: 5
+  retries: 10

# If "Install k8s APT repo GPG key" fails for all nodes
sudo -i
vi /etc/hosts # Add $(hostname -s) for loopback ip 127.0.0.1

# If "Install k8s APT repo GPG key" fails for all nodes
sudo vi /etc/resolv.conf # Add the following nameserver
nameserver 8.8.8.8
nameserver 8.8.4.4 # Or other accepted DNS servers
# Possibly also fix the DNS resolution problem permanently with
# sudo apt-get update && sudo apt-get upgrade -y
```

## Verify the Kubernetes cluster

Checks:
```bash
# ssh to k8s-master as ubuntu
ssh ubuntu@${k8s-master} -A

# Wait for init completed
kubectl get nodes
kubectl get pods --all-namespaces -w

# Grant ubuntu as a docker user
sudo usermod -aG docker centos # sudo groupadd docker
sudo reboot

# ssh to k8s-master as ubuntu
ssh ubuntu@${k8s-master} -A

# Wait for init completed
kubectl get nodes
kubectl get pods --all-namespaces -w

# Check docker
docker ps
```
