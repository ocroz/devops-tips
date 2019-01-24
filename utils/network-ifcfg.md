# Add an IP to the current VM

To add an additional IP address, you need an Ethernet alias. To do this, a consecutive number is simply appended to the interface name, starting with 0 for the first alias. Thus, the first alias of eth0 is eth0:0.

```bash
# /etc/sysconfig/network-scripts/ifcfg-eth0:0
DEVICE=eth0:0
BOOTPROTO=static
BROADCAST=ABC.DEF.GHI.JKL
IPADDR= ABC.DEF.GHI.JKL
NETMASK=255.255.255.255
NETWORK= ABC.DEF.GHI.0
ONBOOT=yes
NM_CONTROLLED=no
```

```bash
DEVICE=eth1
BOOTPROTO=static
BROADCAST=192.168.137.100
IPADDR=192.168.137.100
NETMASK=255.255.255.0
GATEWAY=192.168.137.1
ONBOOT=yes
NM_CONTROLLED=no
```

```bash
sudo systemctl restart network # or sudo reboot
```
