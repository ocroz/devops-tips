# Running Kubernetes Cluster in Docker for Windows

References:
- https://learnk8s.io/blog/installing-docker-and-kubernetes-on-windows
- https://blogs.technet.microsoft.com/stefan_stranger/2018/01/27/running-kubernetes-cluster-in-docker-for-windows/
- https://www.hanselman.com/blog/HowToSetUpKubernetesOnWindows10WithDockerForWindowsAndRunASPNETCore.aspx

Pre-requisites:
- Windows 10 Enterprise
- Hyper-V enabled
- Docker for Windows version 18.06+ installed

Configure `Docker for Windows` with `Kubernetes`:
- Docker for Windows > Settings: Kubernetes > Enable Kubernetes

Configure `kubectl` with `docker-for-desktop` context:
```bash
$ kubectl config get-contexts
CURRENT   NAME                 CLUSTER                      AUTHINFO
          docker-for-desktop   docker-for-desktop-cluster   docker-for-desktop
*         minikube             minikube                     minikube

$ kubectl config use-context docker-for-desktop
Switched to context "docker-for-desktop".

$ kubectl config get-contexts
CURRENT   NAME                 CLUSTER                      AUTHINFO
*         docker-for-desktop   docker-for-desktop-cluster   docker-for-desktop
          minikube             minikube                     minikube
```

Install the alternative (read: [totally insecure](https://github.com/kubernetes/dashboard/wiki/Installation?WT.mc_id=-blog-scottha#recommended-setup)) dashboard:
```bash
# alternative dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/alternative/kubernetes-dashboard.yaml

# charts and graphs too
kubectl create -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/influxdb/influxdb.yaml
kubectl create -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/influxdb/heapster.yaml
kubectl create -f https://raw.githubusercontent.com/kubernetes/heapster/master/deploy/kube-config/influxdb/grafana.yaml

# serve dashboard
kubectl proxy
```

Then open the `Kubernetes Dashboard` on [localhost:8001/ui](http://localhost:8001/api/v1/namespaces/kube-system/services/http:kubernetes-dashboard:/proxy/#!/overview?namespace=default).
