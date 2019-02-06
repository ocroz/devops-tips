# VirtualBox: Create a new VM from a snapshot

## Create the source VM

Create the source VM: Oracle VM VirtualBox > Machine > New...
- Name `base-vbox-centos`,
- Type `Linux`, Version `RedHat (64 bits)`,
- Memory: 1024 MB,
- Create a hard drive now,
- Create

Configure the source VM: Oracle VM VirtualBox > Select the VM > Configuration...
- General > Advanced > clipboard AND drag & drop bidirectional.
- System > Motherboard > Pointing system Multi-Touch USB tablet.
- System > Processor > 2 CPUs.
- Storage > [Controller: IDE] Empty > Optical Drive > Select Optical Drive > Browse and select the Centos 7 ISO file.
- Sound > Deactivate
- Network > Interface 1 as Host-Only network.

### Linux VM installation

VM configuration:

CentOS 7 installation:

See https://www.tenforums.com/tutorials/2291-hyper-v-vm-install-centos-linux-windows-10-a.html
- Timezone and keyboard
- Network and localhost
- Minimal installation
- Default disk partitionning
- User root and user `centos` as administrator
- Reboot

### Network configuration

```bash
# powershell

# Configure the Host-Only network for 192.168.138.0/24
VboxManage list bridgedifs

VboxManage list hostonlyifs
VBoxManage hostonlyif remove "VirtualBox Host-Only Ethernet Adapter #2"
VBoxManage hostonlyif ipconfig "VirtualBox Host-Only Ethernet Adapter" -ip 192.168.138.1

VboxManage list dhcpservers
VboxManage dhcpserver remove --netname "HostInterfaceNetworking-VirtualBox Host-Only Ethernet Adapter"
VboxManage dhcpserver remove --netname "HostInterfaceNetworking-VirtualBox Host-Only Ethernet Adapter #2"

New-NetNat –Name NATNetwork –InternalIPInterfaceAddressPrefix 192.168.138.0/24 –Verbose

# Using the Host's Resolver as a DNS Proxy in NAT Mode
VBoxManage modifyvm "base-vbox-centos" --natdnshostresolver1 on
```

```bash
$ sudo vi /etc/sysconfig/network-scripts/ifcfg-enp0s3
DEVICE=enp0s3
BOOTPROTO=static
BROADCAST=192.168.138.100
IPADDR=192.168.138.100
NETMASK=255.255.255.0
GATEWAY=192.168.138.1
ONBOOT=yes
NM_CONTROLLED=no
```

### User and machine configuration

```bash
# Fix the ssh connection
$ sudo vi /etc/ssh/sshd_config
GSSAPIAuthentication no
UseDNS no

# Then restart sshd
sudo systemctl restart sshd

# Copy your SSH public key into ~centos/.ssh/authorized_keys
vi $HOME/.ssh/authorized_keys
chmod 600 $HOME/.ssh $HOME/.ssh/*
# Exit and ssh again > You should not be prompted for password anymore

# Disable sudo password via
sudo visudo
## Allows people in group wheel to run all commands without password
%wheel  ALL=(ALL)       NOPASSWD: ALL
# Exit and ssh again > You should not be prompted for password at sudo anymore

# Update all the packages
sudo yum update -y

# Put last commands to ease change the IP and rename the hostname later
sudo vi /etc/sysconfig/network-scripts/ifcfg-enp0s3
sudo hostnamectl set-hostname base-vbox-centos;sudo reboot
```

## Clone the VM

Clone the VM: Oracle VM VirtualBox > Machine > Clone...
- Name `xxxx`,
- Mac address politic: Generate new Mac addresses for all interfaces,
- Tick the other options off: Do not preserve disk names and hardware uuid
- Integral clone,
- Clone

### User and machine configuration

Re-run the 2 last commands
