# Kubernetes day 1

VMWare bought Heptio founded by 2 developers from Google.
vSphere will provide Kubernetes soon or later ~2 years.

Separate the head and worker functions on different nodes.
If the head node fails, the applications will continue to function.
Only the reconciliation loop (desired state vs observed state) will not run (control plane).
Restarting the head node is not big deal.

Automated releases of k8s every 3 months of quality thanks to `prow`.

docker has no manifest excepted maybe docker-compose.
Whereas every object in Kubernetes has a manifest.

Put labels in pods to select them.

We can put several containers in one pod such as:
- A microservice
- A logger
- A file watcher
Q: Should we scale the containers at different scales?
A: No -> Keep in same pod, Yes -> Put in separated pods.

manifests:
- rs.yaml: ReplicaSet + Pods
- svc.yaml: Service

```bash
# debug
kubectl run -it --rm debug --image=busybox:1.27 -- /bin/sh
kubectl port-forward pod/what :2368

# Access all ClusterIP services from outside the worker nodes
kubectl proxy &
curl localhost:8001
```

Objects:
- ns
- pod
- rs
- svc: create a dns resolution record
- deployment
- statefulset (previously petset): if deployment order is important
- daemonset (one pod in every node)

Secrets:
Load secret as tmpfs in the container as not saved when the container stops.

host: game.192.168.137.111.nip.io

Create a DNS in Kubernetes for an external database:
https://kubernetes.io/docs/concepts/services-networking/service/
```bash
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: prod
spec:
  type: ExternalName
  externalName: my.database.example.com
```

Sam Newman expert micro-services on oreilly.
