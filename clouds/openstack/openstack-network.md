# Network topology

Network > Router > Subnet > Machine

All the machines behind the same router see their private IPs.<br/>
Otherwise they see their public floating IPs.

*ssh* may take a *long time* to answer although *it may work*.

This message tells you that the network is working.
```bash
$ ssh user@hostname
The authenticity of host 'hostname (hostip)' cannot be established.
ECDSA key fingerprint is SHA256:<...>.
Are you sure you want to continue connecting (yes/no)?
```

The problem might be some unknown configured `DNS Name Servers`.

See the configured DNS Name Servers via this command:
```bash
cat /etc/resolv.conf
```

To permanently change and apply the new DNS Name Servers to all the machines behind the given router:

Go in Openstack GUI > Network > Network topology > Click on the Subnet > On the window that pops up: Click on the Subnet ID > Edit Subnet > Subnet Details > Change the DNS Name Servers.

Example:
```
8.8.8.8
8.8.4.4
```

Then on every machine:
```bash
sudo reboot
```
