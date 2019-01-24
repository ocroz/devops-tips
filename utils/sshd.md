# Configure sshd to speed ssh connection

Scenario:
- Create a Centos 7 VM on hyper-v on your Windows laptop.
- Connect it to the default network switch of type internal.

STEP 1: Fix the ssh connection

```bash
# If ssh takes ages to connect
ssh centos@${hyperv-vm-ip} -vvv # See the errors

# Change the following settings in: /etc/ssh/sshd_config
GSSAPIAuthentication no
UseDNS no

# Then restart sshd
sudo systemctl restart sshd systemd-logind
```

STEP 2: Fix the dns connection

Copy the content of /etc/resolv.conf from WSL to the centos 7 machine but remove the first line to stop regenerate.

Make the changes in /etc/resolv.conf persistent
```bash
# Add these line into: /etc/sysconfig/network-scripts/ifcfg-eth0
RESOLV_MODS="no"
PEERDNS="no"

# Run this command if the file still changes after reboot
chattr +i /etc/resolv.conf
```
