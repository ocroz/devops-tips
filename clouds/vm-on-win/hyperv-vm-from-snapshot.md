# Create a new VM from a snapshot

## Hyper-V

### Create the source VM

Create the source VM: Hyper-V > New > Virtual Machine...
- Name: `base-centos`
- Generation 2
- Memory: 2048 MB
- Network: `Ethernet` (create this new network adapter first)
- Size of new virtual hard disk: 50 GB
- Install OS from bootable `CentOS-7-x86_64-DVD-1804.iso`

Configure the source VM: Hyper-V > Select the VM > Settings...
- Security: Disable the Secure Boot
- Number of virtual processors: 2

Start the source VM & install the OS: Hyper-V > Select the VM > Start & Connect
- Timezone and keyboard
- Network and localhost
- Minimal installation
- Default disk partitionning
- User root and user `centos` as administrator
- Reboot

Get the IP of the machine and update the `hosts` file at localhost:
- Hyper-V > Select the VM > Start
- Hyper-V > Select the VM > Tab `Networking`: Get IP here, or...
- Hyper-V > Select the VM > Connect
- Log as root and get the IP of the machine with command `ip a`.
- (Run as Administrator) Notepad++: `C:\Windows\System32\drivers\etc\hosts`
```bash
172.25.203.180 base-centos
```

Configure the machine before to switch its Network Adapter to `Default Switch`.
```bash
# Log into the machine
ssh centos@base-centos

# STEP 1: Fix the ssh connection

# Change the following settings:
# sudo vi /etc/ssh/sshd_config
GSSAPIAuthentication no
UseDNS no

# Then restart sshd
sudo systemctl restart sshd

# STEP 2: Fix the dns connection

# Copy the content of /etc/resolv.conf from WSL to the centos 7 machine,
# But remove the first line to stop regenerate.
sudo vi /etc/resolv.conf

# To make the changes in /etc/resolv.conf persistent,
# Add the following settings:
# sudo vi /etc/sysconfig/network-scripts/ifcfg-eth0
RESOLV_MODS="no"
PEERDNS="no"

# Run this command if the file still changes after reboot
sudo chattr +i /etc/resolv.conf
```

Exit the machine, then change its Network Adapter to `Default Switch`:
- Hyper-V > `base-centos` > Turn Off...
- Hyper-V > `base-centos` > Settings... > Network: `Default Switch` > Apply
- Hyper-V > `base-centos` > Start
- Get the new machine IP and update the `hosts` file again.

Update the source VM for further use:
```bash
# Log into the machine
ssh centos@base-centos

# Copy your SSH public key into ~centos/.ssh/authorized_keys
vi $HOME/.ssh/authorized_keys
chmod 600 $HOME/.ssh $HOME/.ssh/*
# Exit and ssh again > You should not be prompted for password anymore

# Disable sudo password via
sudo visudo
## Allows people in group wheel to run all commands without password
%wheel  ALL=(ALL)       NOPASSWD: ALL
# Exit and ssh again > You should not be prompted for password at sudo anymore

# Fix the LANG
vi ~/.bashrc # Add: export LANG=en_US.UTF-8

# Add certificates (optional)
sudo vi /etc/ssl/certs/ca-bundle.crt # Add firewall.cer

# Update all the packages
sudo yum update -y

# Put last command to ease rename the hostname later
sudo hostnamectl set-hostname centos;sudo reboot
```

### Checkpoint the source VM and Export the source checkpoint

Checkpoint the source VM:
- Hyper-V > Select the VM > Checkpoint

Export the source checkpoint at `C:\Users\Public\Documents\Hyper-V\VM Exports`:
- Hyper-V > Select the VM > Select the checkpoint > Export

### Create new VM from snapshot

Import new VM: Hyper-V > Import Virtual Machine...
- Select the folder of the exported checkpoint
- Copy the virtual machine (create a new unique ID)
- Keep the `destination` but change the `storage folder` into a tmp directory.

Rename the VM and the vhdx file
- Start & Stop the VM and Rename it
- Rename the vhdx file and move it into the target storage folder
- Then: VM Settings > Select the renamed/moved vhdx file

Get the IP of the machine and update the `hosts` file at localhost:
- Hyper-V > Select the VM > Start
- Hyper-V > Select the VM > Tab `Networking`: Get IP here, or see above

Rename hostname too
```bash
# Log into the machine > You should not be prompted for password
ssh centos@${vm-name}

# Change the hostname (this should be last command)
sudo hostnamectl set-hostname ${vm-name};sudo reboot

# ssh again > the prompt should display the new hostname
ssh centos@${vm-name}
```

Checkpoint the new ${vm-name} to reserve the IP in case any further installation needs to be reseted.
