# Yum repository server

## FTP server

https://serverfault.com/questions/278711/how-to-create-a-yum-repository

```bash
sudo yum install vsftpd -y
sudo systemctl enable vsftpd
sudo systemctl start vsftpd
```

/etc/vsftpd/vsftpd.conf
```bash
anonymous_enable=YES
local_enable=NO # Default YES
write_enable=NO # Default YES
local_umask=022
dirmessage_enable=YES
xferlog_enable=YES
connect_from_port_20=YES
xferlog_std_format=YES
listen=YES # Default NO
listen_ipv6=NO # Default YES
pam_service_name=vsftpd
userlist_enable=YES
tcp_wrappers=YES
# Extra vars
anon_world_readable_only=YES
no_anon_password=YES
# Also open openstack ports 64000-64321
pasv_enable=YES
pasv_min_port=64000
pasv_max_port=64321
port_enable=YES
pasv_address=10.176.227.1
pasv_addr_resolve=NO
```

Add few files under the ftp server:
```bash
sudo vi /var/ftp/hello.txt
```

Test the ftp connection from localhost:
```bash
$ sftp centos@10.176.227.1 # Use the ssh key
ftp> ls
ftp> ^D

$ ftp -p 10.176.227.1
Name (10.176.227.1:crozier): anonymous
ftp> ls
ftp> ^D

$ ftp -np 10.176.227.1
ftp> user anonymous
ftp> ls
ftp> ^D
```

## FTP Yum Repo Mirror

https://opennodecloud.com/howto/2013/12/02/howto-creating-local-yum-repomirror.html
```bash
sudo yum install yum-utils createrepo -y
```

Add 50GB+ volume to the machine:
- See [openstack-volumes](../clouds/openstack/openstack-volumes.md)
- To mount /mnt/yumrepo/mirror at /var/ftp/mirror

/mnt/yumrepo/sync-centos.sh
```bash
#!/usr/bin/bash

BASEDIR=/var/ftp/mirror/centos/7
mkdir -p $BASEDIR
cd $BASEDIR

reposync -n -r updates
repomanage -o -c updates | xargs rm -fv
createrepo updates

reposync -n -r base --downloadcomps
repomanage -o -c base | xargs rm -fv
createrepo base -g comps.xml
```

/mnt/yumrepo/sync-epel.sh
```bash
#!/usr/bin/bash

BASEDIR=/var/ftp/mirror/centos/7
mkdir -p $BASEDIR
cd $BASEDIR

reposync -n -r epel
repomanage -o -c epel | xargs rm -fv
createrepo epel
```

```bash
# CentOS mirror
sudo /mnt/yumrepo/sync-centos.sh

# EPEL mirror
#rpm -ivh http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
curl http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm -o epel-release-latest-7.noarch.rpm
sudo rpm -ivh epel-release-latest-7.noarch.rpm
rm epel-release-latest-7.noarch.rpm
sudo /mnt/yumrepo/sync-epel.sh
```

## FTP Yum Repo Client

```bash
sudo rm /etc/yum.repos.d/*
```

/etc/yum.repos.d/ftp-mirror.repo
```bash
[ftpc7-base]
name=FTP Centos 7 latest base
baseurl=ftp://10.176.227.1/mirror/centos/7/base
enabled=1
gpgcheck=0

[ftpc7-updates]
name=FTP Centos 7 latest updates
baseurl=ftp://10.176.227.1/mirror/centos/7/updates
enabled=1
gpgcheck=0
```

```bash
sudo yum clean all
sudo rm -rf /var/cache/yum
sudo yum update -y
```

Ubuntu:
```bash
# Major release upgrade
sudo do-release-upgrade
# Upgrade packages missed at simple upgrade
sudo rm /boot/grub/menu.lst && sudo update-grub-legacy-ec2 -y &&
  sudo apt-get full-upgrade -y && sudo reboot
# Only security updates
sudo apt-get install unattended-upgrades -y
# "smart" conflict resolution upgrade
sudo apt-get update && sudo apt-get dist-upgrade -y

# Upgrade only currently installed packages
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python-simplejson -y
sudo apt-get autoremove -y # Uninstall the packages not used anymore
```
