# Install and Update packages on Cent OS 7

```bash
rpm -qa | grep package
sudo yum list installed | grep package
sudo systemctl list-unit-files | grep service
sudo yum provides nslookup
sudo yum search perl-
sudo yum search --showduplicates perl-

sudo yum install -y bind-utils
sudo yum update -y && sudo yum autoremove -y
sudo yum remove docker -y

sudo yum clean all
```
