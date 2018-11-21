# Create a new VM from a snapshot

## Hyper-V

### Create the source VM

Create the source VM: Hyper-V > New > Virtual Machine...
- Name: `centos`
- Generation 2
- Memory: 2048 MB
- Network: Ethernet (create this new network adapter first)
- Size of new virtual hard disk: 50 GB
- Install OS from bootable `CentOS-7-x86_64-DVD-1804.iso`

Configure the source VM: Hyper-V > `centos` > Settings...
- Security: Disable the Secure Boot
- Number of virtual processors: 2

Start the source VM and install the OS: Hyper-V > `centos` > Start & Connect
- Timezone and keyboard
- Network and localhost
- Minimal installation
- Default disk partitionning
- User root and user `centos` as administrator
- Reboot

Update the source VM for further use: Hyper-V > `centos` > Start & Connect
- Log as root and get the IP of the machine
```bash
ip a
```
- Update `/etc/hosts` with this new machine at localhost then log via ssh
```bash
ssh centos@centos
```
- Copy your SSH public key into ~centos/.ssh/authorized_keys
```bash
scp you@localhost:$HOME/.ssh/id_rsa.pub centos@centos:$HOME/.ssh/authorized_keys
chmod 600 $HOME/.ssh $HOME/.ssh/*
```
- Exit and ssh again > You should not be prompted for password anymore
```bash
ssh centos@centos
```
- Fix the LANG
```bash
vi ~/.bashrc # Add: export LANG=en_US.UTF-8
```
- Add certificates (optional)
```bash
cd /etc/ssl/certs/
mv ca-bundle.crt _ca-bundle.crt;cp _ca-bundle.crt ca-bundle.crt
vi ca-bundle.crt # Add firewall.cer
```
- Update all the packages
```bash
sudo yum update -y
```
- Put last command to ease rename the hostname later
```bash
sudo hostnamectl set-hostname centos;sudo reboot
```

### Checkpoint the source VM and Export the source checkpoint

Checkpoint the source VM<br/>
Export the source checkpoint at `C:\Users\Public\Documents\Hyper-V\VM Exports`

### Create new VM from snapshot

Import new VM: Hyper-V > Import Virtual Machine...
- Select the folder of the exported checkpoint
- Copy the virtual machine (create a new unique ID)
- Keep the `destination` but change the `storage folder` into a tmp directory.

Rename the VM and the vhdx file
- Rename the VM
- Rename the vhdx file and move it into the target storage folder
- Start & Stop the VM, then: Settings > Select the renamed/moved vhdx file

Start & Connect
- Log as root and get the IP of the machine
```bash
ip a
```
- Update `/etc/hosts` with this new machine at localhost then log via ssh
\> You should not be prompted for password
```bash
ssh centos@${vm-name}
```
- Change the hostname
```bash
sudo hostnamectl set-hostname ${vm-name};sudo reboot
```
- ssh again > the prompt should display the new hostname
```bash
ssh centos@${vm-name}
```

Checkpoint the new ${vm-name} to reserve the IP in case any further installation needs to be reseted.
