# Configuration of consul

See https://www.vaultproject.io/guides/operations/vault-ha-consul.html

```bash
openstack server create --image centos-7-x86_64 --flavor t2.micro --key-name crozier-nagra --security-group ssh-tenant --nic net-id=private consul-sN
```

```bash
sudo yum update -y
sudo yum install unzip -y
sudo yum install bind-utils -y # For dig
```

```bash
CONSUL_VERSION=1.3.0
curl https://releases.hashicorp.com/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip -o consul.zip
sudo unzip consul.zip -d /usr/bin/
rm consul.zip
consul
```

## Start server

In DEV mode (in memory):
```bash
consul agent -dev -bind $(hostname -I)
```

/etc/consul/consul-server.json
```javascript
{
  "server": true,
  "bootstrap_expect": 1,
  "rejoin_after_leave": true,
  "advertise_addr": "192.168.1.61",
  "bind_addr": "192.168.1.61",
  "ports": {
    "grpc": 8502
  },
  "data_dir": "/var/consul",
  "ui_dir": "/var/consul/ui"
}
```

/etc/consul/consul-server.json
```javascript
{
  "server": true,
  //"node_name": "consul_s1",
  "datacenter": "dc1",
  "data_dir": "/var/consul/data",
  "bind_addr": "0.0.0.0",
  "client_addr": "0.0.0.0",
  "advertise_addr": "192.168.1.61",
  "ports": {
    "grpc": 8502
  },
  "bootstrap_expect": 1,
  "ui": true,
  "log_level": "DEBUG",
  "enable_syslog": true,
  "acl_enforce_version_8": false
}
```

```bash
consul agent -config-file /etc/consul/consul-server.json
```

/etc/systemd/system/consul.service
```bash
### BEGIN INIT INFO
# Provides:          consul
# Required-Start:    $local_fs $remote_fs
# Required-Stop:     $local_fs $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Consul agent
# Description:       Consul service discovery framework
### END INIT INFO

[Unit]
Description=Consul server agent
Requires=network-online.target
After=network-online.target

[Service]
User=centos
Group=centos
PIDFile=/var/run/consul/consul.pid
PermissionsStartOnly=true
ExecStartPre=-/usr/bin/mkdir -p /var/run/consul
ExecStartPre=/usr/bin/chown -R centos:centos /var/run/consul
ExecStart=/usr/bin/consul agent \
    -config-file=/etc/consul/consul-server.json \
    -pid-file=/var/run/consul/consul.pid
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
KillSignal=SIGTERM
Restart=on-failure
RestartSec=42s

[Install]
WantedBy=multi-user.target
```

-config-dir=/etc/consul.d

```bash
sudo systemctl start consul
```

## Start agent

/etc/consul/consul-agent.json
```javascript
{
  "ui": true,                       // At ${client_addr}:8500
  "retry_join": ["192.168.1.61"],   // Server IP
  "advertise_addr": "192.168.1.67", // Agent IP
  //"client_addr": "192.168.1.67",    // Default is localhost
  "data_dir": "/tmp/consul"
}
```

/etc/consul/consul-agent.json
```javascript
{
  "server": false,
  "datacenter": "dc1",
  "node_name": "consul_c1",
  "data_dir": "/var/consul/data",
  "bind_addr": "192.168.1.67",
  "client_addr": "127.0.0.1",
  "retry_join": ["192.168.1.61"],
  "log_level": "DEBUG",
  "enable_syslog": true,
  "acl_enforce_version_8": false
}
```

```bash
#export CONSUL_HTTP_ADDR=192.168.1.67:8500 # Unless ${client_addr} is localhost
consul agent -config-file /etc/consul/consul-agent.json
```

## Consul UI/API

UI: http://localhost:8500 <br/>
API: http://localhost:8500/v1/catalog/nodes (see https://www.consul.io/api/index.html)

## DNS API

```bash
consul members
consul operator raft list-peers # There should be no errors
```

```bash
dig @localhost -p 8600 ${SERVER_NAME}.node.consul     # consul-s1.node.consul
dig @localhost -p 8600 ${SERVICE_NAME}.service.consul # consul.service.consul
dig @localhost -p 8600 ${SERVICE_NAME}.service.consul SRV # To get IP & PORT
```

## RPC API

```bash
# First start ${REMOTE_NODE} with:
# consult agent -dev -bind ${IP} -client 0.0.0.0
consul monitor [-rpc-addr=${REMOTE_NODE}:8400]
```

## Registrator

Registrate the service in consul every time a new docker service is up.

## key/value

```bash
curl http://localhost:8500/v1/kv/prod/portal/nginx/?recurse'&'pretty #local
curl http://192.168.1.61:8500/v1/kv/prod/portal/nginx/?recurse'&'pretty #remote
curl http://localhost:8500/v1/kv/prod/portal/nginx/max_fails?raw #raw
```

## consul-template

```bash
CONSUL_TEMPLATE_VERSION=0.19.5
curl https://releases.hashicorp.com/consul-template/${CONSUL_TEMPLATE_VERSION}/consul-template_${CONSUL_TEMPLATE_VERSION}_linux_amd64.zip -o consul-template.zip
sudo unzip consul-template.zip -d /usr/bin/
rm consul-template.zip
consul-template --version
```

/etc/nginx/nginx.conf.ctmpl
```bash
    upstream hwaas {
        {{range service "hwaas-web"}}server {{.Address}}:{{.Port}} max_fails={{key "prod/portal/nginx/max_fails"}} fail_timeout={{key "prod/portal/nginx/fail_timeout"}} weight={{keyOrDefault "prod/portal/nginx/weight" "1"}};
        {{else}}server 127.0.0.1:65535; # force a 502{{end}}
    }
```

/etc/nginx/nginx.conf
```bash
    upstream hwaas {
        server 192.168.1.64:8000 max_fails=2 fail_timeout=30 weight=1;
        server 192.168.1.65:8000 max_fails=2 fail_timeout=30 weight=1;
        server 192.168.1.66:8000 max_fails=2 fail_timeout=30 weight=1;

    }
```

```bash
sudo consul-template -template="/etc/nginx/nginx.conf.ctmpl:/etc/nginx/nginx.conf"
```

/etc/consul/lb.consul-template.hcl
```javascript
template {
  source = "/etc/nginx/nginx.conf.ctmpl"
  destination = "/etc/nginx/nginx.conf"
  command = "sudo systemctl restart nginx"
}
```

```bash
sudo consul-template -config=/etc/consul/lb.consul-template.hcl
```

See how the result file changes when putting a node down in maintenance mode:
```bash
consul maint -http-addr=${REMOTE_NODE}:8500 -enable # -disable
```

See also consul bloking queries:<br/>
https://www.consul.io/api/index.html#blocking-queries

## consul tools

https://www.consul.io/downloads_tools.html

## health check

/etc/consul/web-service.json
```javascript
{
  "service": {
    "name": "hwaas-web",
    "port": 8000,
    "check": {
      "http": "http://localhost:8000",
      "interval": "10s"
    }
  }
}
```

/etc/consul/hc/*-utilization.sh
https://github.com/g0t4/consul-getting-started/tree/master/provision/hc

/etc/consul/web-service.json
https://github.com/g0t4/consul-getting-started/blob/master/provision/web-consul.d/hc.json

```bash
consul agent -config-file /etc/consul/consul-agent.json \
    -config-file /etc/consul/web-service.json \
    -config-file /etc/consul/health-check.json -enable-script-checks=true
```

```bash
sudo yum install unzip bc stress -y
stress -c 1
```
