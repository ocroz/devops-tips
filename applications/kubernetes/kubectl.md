# Pilot your kubernetes cluster with kubectl

Check you kubectl config:
```bash
vi $HOME/.kube/config
```

Connect to the cluster:
```bash
kubectl version
kubectl config get-contexts
kubectl config use-context docker-for-desktop # minikube
kubectl config current-context
```

Run hello-world:<br/>
See https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address/
```bash
# possibly pull docker image first
docker pull gcr.io/google-samples/node-hello:1.0
docker ps

# Deploy the service
kubectl run hello-world --replicas=5 --labels="run=load-balancer-example" --image=gcr.io/google-samples/node-hello:1.0 --port=8080
kubectl get deployments hello-world
kubectl get replicasets
kubectl get pods # --all-namespaces
kubectl get all  # --all-namespaces

# Expose the service
kubectl expose deployment hello-world --type=LoadBalancer --name=hello-world-service
# --type=NodePort
kubectl get services hello-world-service

# powershell (in case EXTERNAL-IP still pending with minikube)
minikube service hello-world-service

# Cleaning
kubectl delete services hello-world-service
kubectl delete deployment hello-world
```

Pull a nodejs docker container:
```bash
git clone https://github.com/IBM/dWTVSimpleContainerApp
```

## Next

- From `kubectl run` to `kubectl create` + `kubectl apply`.
- Be declarative with yaml manifest files + git everything.
- Use deployments for rolling upgrades and rollbacks to recorded revisions.
  pods > replica sets > deployments > service.

- Load Balancer.
- HA with etcd and control planes.
- Master docker.
