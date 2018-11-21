# Kubernetes cluster on openstack

References:
- https://docs.openstack.org/senlin/latest/user/clusters.html

```bash
pip install python-openstacksdk senlin python-senlinclient
# pip uninstall python-openstacksdk senlin python-senlinclient

openstack cluster list # openstack cluster profile list
# public endpoint for clustering service not found
openstack service list
# You are not authorized to perform the requested action: identity:list_services (HTTP 403)
openstack endpoint list
# You are not authorized to perform the requested action: identity:list_endpoints (HTTP 403)
```
