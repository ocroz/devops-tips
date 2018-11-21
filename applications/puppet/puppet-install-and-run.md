# Install puppet

See https://www.digitalocean.com/community/tutorials/how-to-install-puppet-4-in-a-master-agent-setup-on-centos-7

## Add certificates (optional)

```bash
cd /etc/ssl/certs/
mv ca-bundle.crt _ca-bundle.crt;cp _ca-bundle.crt ca-bundle.crt
vi ca-bundle.crt # Add firewall.cer
```

## Puppet Server

```bash
visudo
usermod -aG wheel puppet
su - puppet
```

Also adjust the VM memory:
```bash
sudo rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm
sudo yum -y install puppetserver
sudo vi /etc/sysconfig/puppetserver # JAVA_ARGS="-Xms3g -Xmx3g"
```

```bash
sudo service puppetserver start;echo $?
sudo service puppetserver status # systemctl status puppetserver.service
sudo service puppetserver stop;journalctl -xe
```

```bash
sudo chown -R puppet:puppet /etc/puppetlabs/
sudo systemctl enable puppetserver
ps -aux | grep -v grep | grep puppet
```

```bash
ls /etc/sysconfig/puppet*
ls /etc/puppetlabs/puppet/
find /etc/puppetlabs/ -type f
```

## Puppet Agent

```bash
sudo rpm -ivh https://yum.puppetlabs.com/puppetlabs-release-pc1-el-7.noarch.rpm
sudo yum -y install puppet-agent
```

```bash
service puppet status # restart
```

```bash
sudo /opt/puppetlabs/bin/puppet resource service puppet ensure=running enable=true
ps -aux | grep -v grep | grep puppet
```

## Puppet Communication

https://puppet.com/docs/puppet/5.3/quick_start_master_agent_communication.html
https://puppet.com/docs/puppet/5.3/config_file_main.html

- Modifying the /etc/hosts files
- Opening port 8140 on Puppet Master firewall
- Sign Certificates on Puppet Master

On Master
```bash
iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport 8140 -j ACCEPT
```

On Agent:
```bash
/opt/puppetlabs/bin/puppet agent --test
```

On Master:
```bash
sudo /opt/puppetlabs/bin/puppet cert sign|list --all
sudo touch /etc/puppetlabs/code/environments/production/manifests/site.pp
```

On Agent:
```bash
/opt/puppetlabs/bin/puppet agent --test
/opt/puppetlabs/bin/facter
```

## Push a configuration

On Master:/etc/puppetlabs/code/environments/production/manifests/site.pp
```bash
node '<agent>' {
  file {'/tmp/example-ip':
    ensure  => present,
    mode    => '0644',
    content => "Here is my Public IP Address: ${ipaddress}.\n",
  }
}
```

On Agent:
```bash
/opt/puppetlabs/bin/puppet agent --test
cat /tmp/example-ip
```

## Puppet environments and modules

See https://www.digitalocean.com/community/tutorials/getting-started-with-puppet-code-manifests-and-modules

The master uses the central manifest as configured, see:
```bash
sudo /opt/puppetlabs/bin/puppet master --configprint manifest
sudo /opt/puppetlabs/bin/puppet config print manifest modulepath --section master --environment production # or test
```

Test and apply the new configuration after each change (see changes below):
```bash
sudo /opt/puppetlabs/bin/puppet apply --test # Ctrl^C if no error
sudo service puppetserver restart;echo $?
```

Main configuration on master:<br/>
/etc/puppetlabs/puppet/puppet.conf
```bash
[main]
  server = <master>
  certname = <master>
  dns_alt_names = <master>.publicdomain,<master>.localdomain,<master>,puppet.localdomain,puppet
  autosign = false
  trusted_node_data = true
  environmentpath = $confdir/environments

[master]
  node_terminus = exec
  external_nodes = /etc/puppetlabs/puppet/node.sh
  vardir = /opt/puppetlabs/server/data/puppetserver
  logdir = /var/log/puppetlabs/puppetserver
  rundir = /var/run/puppetlabs/puppetserver
  pidfile = /var/run/puppetlabs/puppetserver/puppetserver.pid
  codedir = /etc/puppetlabs/code
```

Define which node has which environment:<br/>
/etc/puppetlabs/puppet/node.sh
```bash
#!/bin/bash
case "$1" in
  "<agent-01>" |\
  "<agent-02>" )
    echo "environment: test";;
  *)
    echo "environment: production";;
esac
```

Environment settings for production:<br/>
/etc/puppetlabs/puppet/environments/production/environment.conf
```bash
manifest = $confdir/environments/production/manifests
modulepath = $confdir/environments/production/modules:$confdir/modules:/usr/share/puppet/modules
#config_version = /usr/bin/git --git-dir $confdir/environments/production/.git rev-parse HEAD
```

Environment settings for test:<br/>
/etc/puppetlabs/puppet/environments/test/environment.conf
```bash
manifest = $confdir/environments/test/manifests
modulepath = $confdir/environments/test/modules:$confdir/modules:/usr/share/puppet/modules
#config_version = /usr/bin/git --git-dir $confdir/environments/test/.git rev-parse HEAD
```

Add a single manifest in production (see below for test):<br/>
/etc/puppetlabs/puppet/environments/production/manifests/site.pp
```bash
node '<agent-02>' {
  file {'/tmp/example-ip':
    ensure  => present,
    mode    => '0644',
    content => "Here is my Public IP Address: ${ipaddress}.\n",
  }
}
```

In test, either create a single manifest:<br/>
/etc/puppetlabs/puppet/environments/test/manifests/class_example.pp
```bash
class example_class {
  file {'/tmp/example-ip':
    ensure  => present,
    mode    => '0644',
    content => "CLASS TEST> Here is my Public IP Address: ${ipaddress}.\n",
  }
}
```

Or create a module:<br/>
/etc/puppetlabs/puppet/environments/test/modules/example/manifests/init.pp
```bash
class example {
  file {'/tmp/example-ip':
    ensure  => present,
    mode    => '0644',
    content => "MODULE TEST> Here is my Public IP Address: ${ipaddress}.\n",
  }
}
```

Then include the manifest and/or the module:<br/>
/etc/puppetlabs/puppet/environments/test/manifests/site.pp
```bash
node '<agent-02>' {
  # either use a normal class declaration like: include example_class
  include example_class # *.pp are loaded in alphabetic order

  # or use a resource-like class declaration like: class { 'example_class': }
  # this allows to specify class parameters

  # include example # modules are loaded first
}
```

## Pre-existing modules

See https://forge.puppetlabs.com/

```bash
sudo /opt/puppetlabs/bin/puppet module install <module> --environment production # or test
```

Then include it as above.
