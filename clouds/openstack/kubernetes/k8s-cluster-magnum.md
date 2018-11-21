# Kubernetes cluster on openstack

References:
- https://cloudbase.it/easily-deploy-a-kubernetes-cluster-on-openstack/
- https://docs.openstack.org/magnum/latest/user/index.html
- https://docs.openstack.org/newton/user-guide/common/cli-install-openstack-command-line-clients.html

```bash
# sudo apt install -y python-magnumclient python-neutronclient
# sudo apt --purge autoremove -y python-magnumclient python-neutronclient
pip install python-magnumclient python-neutronclient python-heatclient
# pip uninstall -y python-magnumclient python-neutronclient python-heatclient
which openstack nova neutron magnum heat

# sudo apt install -y qemu-utils
# sudo apt --purge autoremove -y qemu-utils
# which qemu-img
```

```bash
cd images
wget  https://ftp-stud.hs-esslingen.de/pub/Mirrors/alt.fedoraproject.org/atomic/stable/Fedora-Atomic-25-20170512.2/CloudImages/x86_64/images/Fedora-Atomic-25-20170512.2.x86_64.qcow2

openstack image create --public --property os_distro='fedora-atomic' --disk-format qcow2 --container-format bare --file Fedora-Atomic-25-20170512.2.x86_64.qcow2 fedora-atomic.qcow2
# 403 Forbidden: You are not authorized to complete this action. (HTTP 403)

neutron net-create public_net --shared --router:external --provider:physical_network physnet2 --provider:network_type flat
# The request you have made requires authentication. (HTTP 401)

magnum cluster-template-create --name "k8s-cluster-template" \
  --image "fedora-27-x86_64" --keypair "crozier-MOB100326" \
  --external-network "k.grp" --dns-nameserver "8.8.8.8" --flavor "t2.small" \
  --docker-volume-size "3" --network-driver "flannel" --coe "kubernetes"
# ERROR: public endpoint for container service not found

heat stack-list
# The request you have made requires authentication. (HTTP 401)
```
