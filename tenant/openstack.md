# Configuration of openstack

## Installation
### Base VM

```bash
openstack server create --image centos-7-x86_64 --flavor t2.micro --key-name crozier-nagra --security-group ssh-tenant --nic net-id=private openstack
```

```bash
sudo yum update -y
```

### pip

```bash
sudo yum install -y epel-release
sudo yum upgrade python-setuptools
sudo yum install -y python-pip python-wheel python-devel
sudo yum groupinstall -y "Development tools"
sudo pip install --upgrade pip
```

### ansible for openstack

```bash
sudo pip install shade --ignore-installed
sudo yum install -y ansible
```

### openstack client

```bash
sudo pip install python-openstackclient --ignore-installed
```

## Create new VM
### With ansible

Configure git:
```bash
git config --global user.name "Olivier Crozier"
git config --global user.email olivier.crozier@nagra.com
curl -O https://raw.githubusercontent.com/deliciousinsights/support-files/master/config-git.sh
source ./config-git.sh # First add firewall.cer in ./curl-ca-bundle.crt
# .bash_profile: source /usr/share/git-core/contrib/completion/git-prompt.sh
```

As long as your ssh private key has been forwarded:
```bash
git clone git@git.kudelski.com:cm-admin-team/ansible-playbooks.git
cd ansible-playbooks/
git checkout develop
cd new-vm/
vi inventories/group_vars/all.yaml
vi playbooks/create_os_vm.yaml
ansible-playbook -i inventories/inventory playbooks/create_os_vm.yaml
```

### With openstack
#### Configuration

```
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

#### Connection

```bash
export OS_CLOUD=eu-zrh-cas-cmadmin-dev
source openstack-password.sh
openstack token issue
openstack server create --image centos-7-x86_64 --flavor t2.micro --key-name crozier-nagra --security-group ssh-tenant --nic net-id=private consul-s1
```

#### Create new machine

```bash
openstack server create --image "centos-7-x86_64" --flavor "t2.micro" \
  --key-name "crozier-nagra" --security-group "ssh-tenant,other" \
  --nic net-id="private" "hostname"
openstack server list
```
