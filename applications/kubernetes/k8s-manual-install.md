# Getting Started With Kubernetes On Centos 7 Using Manual Installation

References:
- https://kubernetes.io/docs/setup/independent/install-kubeadm/ +next
- https://www.linuxtechi.com/install-kubernetes-1-7-centos7-rhel7/
- https://www.howtoforge.com/tutorial/centos-kubernetes-docker-cluster/
- https://docs.projectcalico.org/v3.1/getting-started/kubernetes/

Every node (master and minions) needs:
- docker
- kubelet
- kubeadm
- kubectl
- CNI

On all k8s master and node servers:
```bash
# As root
sudo su -

# Disable SWAP
swapoff -a && vi /etc/fstab # Comment the swap line UUID

# Install Docker
yum install docker -y
docker --version

# Make user centos a docker user on all nodes:
groupadd docker
usermod -aG docker centos
reboot

# Install Kubernetes
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kube*
EOF

# Set SELinux in permissive mode (effectively disabling it)
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

systemctl start docker && systemctl enable docker
systemctl start kubelet && systemctl enable kubelet

# To fix issues with traffic being routed incorrectly due to iptables being bypassed
cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sysctl --system

# Start the services docker and kubelet
systemctl restart docker
systemctl restart kubelet

# Change the cgroup-driver
docker info | grep -i cgroup
vi /etc/default/kubelet
KUBELET_KUBEADM_EXTRA_ARGS=--cgroup-driver=systemd
systemctl daemon-reload && systemctl restart kubelet
```

On k8s master server:
```bash
# As root
sudo su -

# Open ports
iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport 6443 -j ACCEPT
iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport 10250 -j ACCEPT

# Create the master
kubeadm init
# kubeadm init --pod-network-cidr=192.168.0.0/16 # If using calico network
```

On k8s master server:
```bash
# As centos
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

vi ~/.bashrc # Add the above line too
export KUBECONFIG=$HOME/.kube/config

kubectl get nodes
kubectl get pods --all-namespaces # if NotReady

# Apply network configuration: Weave Net
sudo sysctl net.bridge.bridge-nf-call-iptables=1
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

# If using calico network
#kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/rbac-kdd.yaml
#kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml
## kubectl apply -f https://docs.projectcalico.org/v3.1/getting-started/kubernetes/installation/hosted/kubeadm/1.7/calico.yaml
```

Open port 6443 on all nodes, then...<br/>
On k8s minion servers:
```bash
kubeadm join ${master}:6443 --token ${tk} --discovery-token-ca-cert-hash ${sha}
```

```bash
kubeadm join 192.168.1.68:6443 --token 89pmdb.c5deqrk0spih501s --discovery-token-ca-cert-hash sha256:389f35dcb5a94984654d76688cc6a81474f6391f452507507541d004ff4e1ac8
kubeadm join 10.0.10.91:6443 --token 8p2kcm.hrbfuogsfruiddfk --discovery-token-ca-cert-hash sha256:6693c51bf04fc25b6e2f4a149be9e9ffd1353c955e4a6a95bb80a2b18daf4b3b
```
https://github.com/kubernetes/kubeadm/issues/975

Fix kubelet problem on all nodes:<br/>
See https://github.com/kubernetes/kubernetes/issues/56850
```bash
journalctl -xe # unknown container "/system.slice/kubelet.service"
journalctl -u kubelet.service

sudo vi /etc/sysconfig/kubelet
KUBELET_EXTRA_ARGS= --runtime-cgroups=/systemd/system.slice --kubelet-cgroups=/systemd/system.slice
sudo systemctl restart kubelet
```

Then https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/

PROBLEMS:
- Cannot expose a public IP
- Cannot start the Kubernetes Dashboard
