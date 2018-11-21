# Fixing pip issues inside virtualenv on Ubuntu

Steps:
- Uninstall Ubuntu 18.04
- Install Ubuntu 18.04
```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo vi /etc/ssl/certs/ca-certificates.crt # Add firewall.hq.k.grp
```

Install virtualenv
```bash
sudo apt-get install build-essential virtualenv python-virtualenv python-dev
#sudo apt-get install python-setuptools git
```

If getting SSLError(SSL: CERTIFICATE_VERIFY_FAILED) at `pip install`:
```bash
virtualenv openstack
source openstack/bin/activate
pip install python-openstackclient ansible shade
```

$HOME/openstack/pip.conf
```
[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
```

`pip install` should work again.
```bash
pip install --upgrade pip
pip install python-openstackclient python-openstacksdk ansible shade
```
