# Getting Started With Kubernetes On Windows 10 Using HyperV And MiniKube

References:
- https://www.c-sharpcorner.com/article/getting-started-with-kubernetes-on-windows-10-using-hyperv-and-minikube/
- https://github.com/kubernetes/minikube/issues/2976
- https://github.com/kubernetes/minikube/issues/1408
- https://github.com/kubernetes/minikube/issues/1815#issuecomment-343974572

Download KukeCtl and Minikube for Windows and rename them as:<br/>
`C:\Program Files\Kubernetes\client\bin\kubectl.exe`<br/>
`C:\Program Files\Kubernetes\Minikube\minikube.exe`<br/>
Or use the `kubectl.exe` supplied with `docker-for-desktop`.

```bash or powershell
kubectl version
minikube version
```

Start minikube as an administrator:
```powershell
# Alias minikube to force using the "kubeadm bootstrapper"
$EnvMinikube = "${Env:ProgramFiles}\Kubernetes\Minikube\minikube.exe"
function minikube { cmd /c $EnvMinikube --bootstrapper=kubeadm $args }

# The "localkube bootstrapper" is deprecated
#function minikube { cmd /c $EnvMinikube --bootstrapper=localkube $args }
#minikube config set ShowBootstrapperDeprecationNotification false

# Start cluster
minikube start --vm-driver=hyperv --kubernetes-version="v1.10.3" --hyperv-virtual-switch="Ethernet" --memory 4096 --cpus=2
# --kubernetes-version="v1.12.1"
# --hyperv-virtual-switch="Wireless" or "nat"
# --docker-env HTTP_PROXY=http://${host:port} --docker-env HTTPS_PROXY=${https}
# --v=7 --alsologtostderr

# Add certificates (optional) (See below ```bash section)
# - Required if behing a corporate proxy
# - Do it as soon as you can get the VM IP via Hyper-V

# Verify cluster nodes and pods
minikube status # Should be Running + Running + Minikube IP

# In a separate bash
kubectl config use-context minikube
kubectl get nodes # Status should be Ready
kubectl get pods --all-namespaces # All should be Running
```

Add certificates (optional):
```bash
# In a separate bash
ssh docker@${MiniKube-IP} # password = tcuser
$ sudo vi /etc/ssl/certs/ca-certificates.crt # Add firewall.cer
$ sudo systemctl restart docker # Apply the new certificate
$ sudo swapoff -a # Possibly disable swap memory too

# Wait until all the ~23 docker containers are pulled and the pods running
$ docker ps | wc -l
# In a separate bash
kubectl get pods --all-namespaces # All should be Running
```

Minikube commands:
```powershell
minikube status # start
minikube stop   # + minikube ssh > sudo poweroff
minikube delete # + Remove-Item $env:USERPROFILE\.minikube -Force -Recurse
minikube logs
minikube ssh
minikube dashboard
minikube docker-env
export DOCKER_TLS_VERIFY=1; export DOCKER_HOST=tcp://${MiniKubeIP}:2376; export DOCKER_CERT_PATH=$HOME/.minikube/certs; export DOCKER_API_VERSION=1.35;
minikube service <service> # Expose the pending service outside minikube
```

Problems with MiniKube:
- Not as plug-and-play and as fast as `docker-for-desktop` with kubernetes.
- Not easy nor even possible to work behind a proxy: docker pull hello killed.
- Not usable at work and home: the certificate is not valid for the other IP.
