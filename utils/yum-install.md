# Install and Update packages on Cent OS 7

```bash
rpm -qa | grep package
sudo yum list installed | grep package
sudo systemctl list-unit-files | grep service
sudo yum provides nslookup
sudo yum search perl-
sudo yum search --showduplicates perl- # List all available versions that can be installed of perl-

sudo yum install -y bind-utils
sudo yum update -y && sudo yum autoremove -y
sudo yum remove docker -y

sudo yum clean all
sudo yum makecache
```

# Install and Update packages on Ubuntu

```bash
sudo apt search docker-compose
sudo apt install docker-compose -y # docker-compose=x.y.z
```
