# Deploy Artifactory via puppet

References:
- https://jfrog.com/open-source/
- https://forge.puppet.com/autostructure/artifactory
- https://www.jfrog.com/confluence/display/RTF/Installing+Artifactory (Watch the Screencast)

```bash
puppet module install autostructure-artifactory --version 2.0.13 --environment test
```

```bash
/opt/jfrog/artifactory/bin/artifactoryctl check
service artifactory status
tail -f /var/opt/jfrog/artifactory/logs/artifactory.log
curl http://admin:password@<host>:8081/artifactory/api/system/configuration
curl http://<host>:8081/artifactory
```

```bash
vi /etc/opt/jfrog/artifactory/default # Adjust Xmx and START_TMO
```

```bash
iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport 8081 -j ACCEPT
```

Start Artifactory in the browser, and do the initial configurations

Proxy Key: local-proxy
Host: http://devops-02.localdomain
Port: 8888

Group: contributors
User: guest in group contributors
Permission: Contributors gives contributors Deploy/Cache permission to any repo
