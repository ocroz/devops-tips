# Training Puppet Language Basics

https://learn.puppet.com/course/puppet-language-basics

```bash
runbook

package { 'openssh-server':
  ensure => installed,
}
puppet resource package puppet

file { '/var/lib/pgsql/data/postgresql.conf':
  ensure  => 'file',
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  content => "listen_addresses = '192.168.0.10'",
}
puppet resource file /var/lib/pgsql/data/postgresql.conf

facter -p # ~environment variables

service { 'sshd':
  ensure => running,
  enable => true,
}
puppet resource service puppet

# manifest file postgresql.pp
class postgresql {
  $package_name = 'postgresql-server'
  $service_name = 'postgresql'
  package { '${package_name}':
    ensure => installed,
  }
  file { '/var/lib/pgsql/data/postgresql.conf':
    ensure  => file,
    content => '...',
    require => Package['${package_name}'], # or use before on package
    notify  => Service['${service_name}'], # or use subscribe on service
  }
  service { '${service_name}':
    ensure  => running,
    enable  => true,
  }
}
node 'pgsql.org.com' {
  include postgresql # or class {'postgresql:'}
}
puppet parser validate postgresql.pp
```
