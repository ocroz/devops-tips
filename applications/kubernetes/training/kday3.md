# Install Kubernetes manually

Install a head node:
https://github.com/sebgoa/oreilly-kubernetes/blob/master/scripts/k8s.sh

Switch your head as worker node
https://kubernetes.io/docs/reference/setup-tools/kubeadm/kubeadm-reset/
```bash
# On master
kubeadm token create --print-join-command

# On worker: Run the above printed command
```

## Install add-ons

```bash
$ sudo netstat --inet --inet6 -pan | grep 6783
tcp   0  0  172.31.25.209:47339  172.31.17.117:6783  ESTABLISHED  24507/weaver
tcp   0  1  172.31.25.209:52021  172.31.20.251:6783     SYN_SENT  24507/weaver
tcp6  0  0  :::6783              :::*                     LISTEN  24507/weaver
tcp6  0  0  172.31.25.209:6783   172.31.17.22:44049  ESTABLISHED  24507/weaver
udp   0  0  0.0.0.0:6783         0.0.0.0:*                        24507/weaver
# SYN_SENT shows a firewall issue (blocked port)
```

```powershell
Set-VMProcessor -VMName k8s-minikube -ExposeVirtualizationExtensions $true
```
