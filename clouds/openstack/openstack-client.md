# On openstack

## Installation

```bash
# We need to upgrade or we cannot install virtualenv
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential virtualenv python-virtualenv python-dev

virtualenv openstack
source openstack/bin/activate
pip install python-openstackclient

which openstack nova
openstack --version

sudo mkdir /etc/openstack && sudo vi /etc/openstack/clouds-public.yaml
```

```yaml
public-clouds:
  eu-zrh:
    auth:
      auth_url: https://cloud.eu-zrh.hub.kudelski.com:5000/
  us-phx:
    auth:
      auth_url: https://cloud.us-phx.hub.kudelski.com:5000/
```

```bash
mkdir -p ~/.config/openstack && vi ~/.config/openstack/clouds.yaml
```

```yaml
clouds:
  eu-zrh-cas-cmadmin-dev:
    profile: eu-zrh
    identity_api_version: '3'
    interface: public
    auth:
      domain_name: hq.k.grp
      project_name: cas-cmadmin-dev
      username: olivier.crozier@nagra.com
```

```bash
mkdir bin; vi bin/openstack-password.sh; chmod 755 bin/openstack-password.sh
```

```bash
echo "Please enter your OpenStack Password: "
read -sr OS_PASSWORD_INPUT
export OS_PASSWORD=$OS_PASSWORD_INPUT
```

## Connection

```bash
source openstack/bin/activate
source openstack-password.sh
export OS_CLOUD=eu-zrh-cas-cmadmin-dev
openstack token issue
```

## Create new machine

```bash
openstack server create --image "centos-7-x86_64" --flavor "t2.small" \
  --key-name "crozier-MOB100326" --security-group "ssh,other" \
  --nic net-id="private" "hostname"
openstack server list
```
