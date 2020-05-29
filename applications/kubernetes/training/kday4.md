# Securize your pipeline

Dev: Best practices on containers:
- non root
- only what you need

Registry: continuous scanning
- containers
- npm, etc

Pod: spec
- security context
- capabilities
- namespace

Attacker in the pod:
- Can he talk to the API server?
  Yes: every pod has a `service account` = default

RBAC:

```bash
kubectl -n $namespace get serviceaccount -o yaml # get secret
kubectl -n $namespace describe secret $secret # get token
https://jwt.io/ # decode the token
kubectl -n $namespace exec -it $pod sh # enter the nginx pod
> apt update
> apt install curl -y
> curl -k https://kubernetes.default:443 # anonymous
> token=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
> curl -k -H "Authorization: Bearer $token" https://kubernetes.default:443
```

Example: https://github.com/helm/charts/tree/master/stable

RBAC:
```bash
kubectl -n $ns get sa # get service accounts
kubectl -n $ns get roles # get roles
kubectl -n $ns get rolebindings # get role bindings
kubectl -n $ns --as=system:serviceaccount:$ns:$sa auth can-i get pods

kubectl -n $ns exec -it $pod sh # enter the nginx pod
> token=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
> h="Authorization: Bearer $token"
> ns=default
> curl -k -H "$h" https://kubernetes.default/api/v1/namespaces/$ns/pods

# https://github.com/aquasecurity/kubectl-who-can
kubectl-who-can get pods -n $ns
```

Role binding has a kind User. However there's no User object in k8s.
We must authenticate against a CN x509 certificate, linked to SAML...

Installation:
- Kubernetes
- Addon: Network -> Control the iptables and ebtables
  | Weave: ok
  | Calico: bigger installations
- Addon: Network Policy Controller
  | Possibly already included in addon network, such as with weave (pod two)
- Addon: Ingres Controller

Pod Security Policy (PSP) is being deprecated.
Now use a dynamic admission controller... or OPA.

https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/
