# Install saltstack

References:
- https://app.pluralsight.com/player?course=salt-getting-started

## Steps

### Ports

See https://docs.saltstack.com/en/latest/topics/tutorials/firewall.html

On master:
```bash
sudo iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport 4505 -j ACCEPT
sudo iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport 4506 -j ACCEPT
```

### Bootstrap

See https://docs.saltstack.com/en/latest/topics/tutorials/salt_bootstrap.html

```bash
curl -L https://bootstrap.saltstack.com -o bootstrap-salt.sh
sudo sh bootstrap-salt.sh -M -A 127.0.0.1 # Master + Local Minion
sudo sh bootstrap-salt.sh -A ${master-ip} # Remote Minion [-I <minion-name>]
```

### Keys

```bash
(master) $ sudo salt-key                      # List keys
(master) $ sudo salt-key -f <minion-name>     # Show this key

(minion) $ sudo salt-call --local key.finger  # Compare to true minon key

(master) $ sudo salt-key -a <minion-name> -y  # Accept this key
```

### Targeting Minions in Groups

```bash
sudo service salt-minion stop|start
sudo salt '*' test.ping # Or any wildcards
sudo salt node* test.ping
sudo salt node1? test.ping
sudo salt node[123] test.ping
sudo salt -E '(master|node*)' test.ping
sudo salt -S 192.168.0.0/16 test.ping
sudo salt -C 'S@192.168.0.0/16 and E@(master|node*)' test.ping
sudo salt -C 'G@roles:web' test.ping
```

### Execution Modules

See https://docs.saltstack.com/en/latest/salt-modindex.html<br/>
Example: [SALT.MODULES.CMDMOD](https://docs.saltstack.com/en/latest/ref/modules/all/salt.modules.cmdmod.html#module-salt.modules.cmdmod).

```bash
sudo salt '*' cmd.run 'whoami;pwd;ls' # 'run' command from 'cmd' module
```

## States

```bash
mkdir /srv/salt
```

/srv/salt/top.sls
```yaml
base:
  'p4-git-tst':
    - helix-p4d-package
```

/srv/salt/helix-p4d-package.sls
```yaml
helix-p4d:
  pkg:
    - installed
```

Apply state to the minions:
```bash
sudo salt 'p4*' state.apply
```

Debug commands on the minion:
```bash
sudo salt-call cp.list_master
sudo salt-call cp.get_file_str salt://top.sls
sudo salt-call -l debug state.apply
```

## Grains

Grains are stored on the minions.

```bash
# Get all grains or specific grain
sudo salt ${minions} grains.get [${grain-key}]
# Set unique value
sudo salt ${minions} grains.set ${grain-key} ${grain-value}
# Delete grain value and key
sudo salt ${minions} grains.delkey ${grain-key}
# Add/Remove value in grain array
sudo salt ${minions} grains.append ${grain-key} ${grain-value}
sudo salt ${minions} grains.remove ${grain-key} ${grain-value}
```

## Pillars and Templating

Pillars are stored on the master.

```bash
sudo salt '*' pillar.items
sudo salt '*' pillar.obfuscate
sudo salt '*' pillar.get ${key}
```

```bash
mkdir /srv/pillar
```

/srv/pillar/top.sls
```yaml
base:
  'roles:load-balancing':
    - match: grain
    - hwaas-ssl
```

/srv/pillar/hwaas-ssl.sls
```yaml
hwaas-ssl:
  cert-path:
    /etc/nginx/hwaas.local.crt
  cert-key-path:
    /etc/nginx/hwaas.local.crt.key
  cert-contents: |
    -----BEGIN CERTIFICATE-----
    -----END CERTIFICATE-----
  cert-key-contents: |
    -----BEGIN RSA PRIVATE KEY-----
    -----END RSA PRIVATE KEY-----
```

Apply state to the minions:
```bash
sudo salt 'roles:load-balancing' state.apply
```

## Mining

```bash
sudo salt -G 'roles:web' saltutil.refresh_pillar
sudo salt -G 'roles:web' mine.update
sudo salt-call mine.get '*' hwaas-webserver-addr
```

## Orchestration

```bash
sudo salt-run state.orch orch.new-webserver pillar='{"target-minion": "web3"}'
```

## Troubleshooting

- https://github.com/saltstack/salt/issues/13080
