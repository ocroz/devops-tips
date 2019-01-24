# Create a local network for Hyper-V

## Network cleanup

```bash
# powershell
arp -a
NetSh Int IP Delete ARPCache
netsh int ip reset
```

Remove all or any useless network adapters
- Control Panel > Device Manager
- MACHINE > Network adapters > Uninstall all Hyper-V Virtual Ethernet Adapters

Reset network + Restart Windows
- Windows > Settings > Network & Internet > Network reset > Reset now
This recreates the missing needed network adapters

## Create new subnet with fixed ip for localhost

Create the virtual switch in Hyper-V
- Hyper-V > Virtual Switch Manager... > New virtual network switch
- Select `internal` > Create Virtual Switch > Name = `hypervnat` > Apply & OK

Inspect the new network via powershell
```bash
ipconfig # Gives the IPV4 address for `hypervnat`
ipconfig /all | find /i "DHCP Server" # Gives the DHCP server IP address
route print -4 # Gives the IPV4 defined routes
#route -p ADD 169.254.54.254 MASK 255.255.0.0 192.168.0.254
#route DELETE 169.254.54.254
```

Fix the ip for localhost
- Control Panel > Network and Sharing Center > Change adapter settings
- Select `hypervnat` > Properties
- Select "Internet Protocal 4 (TCP/IPv4)" > Properties
- Select "Use the following IP address"
  IP address = The IPV4 address you got from "ipconfig"
  Default gateway = XXX.XXX.XXX.254
  First prefered DNS server = The DHCP IP address you got from "ipconfig /all"
  Advanced: Possible cleaning + List more DNS servers
  OK

## Configure the VM with 2 network adapters

- Network Adapter 1 = `Default Switch` to get the Internet.
- Network Adapter 2 = `hypervnat` to get a fixed IP.

- Hyper-V > MACHINE > Settings...
- Add Hardware > Network Adapter > Add
- Virtual Switch = `hypervnat` > Apply & OK

## SOLUTION 1 : Use a local DHCP server

### Local DHCP server

- Download http://www.dhcpserver.de/cms/download/ & unzip into `C:\dhcpserver`.
- Run C:\dhcpserver\dhcpwiz.exe
- Next > Select `hypervnat` > Next > Next
- IP-Pool = XXX.XXX.XXX.100-200 > Next > Write INI file > Cancel
- Run C:\dhcpserver\dhcpsrv.exe > Admin
- Install + Start + Configure

### When your laptop connects to another physical network

- Run C:\dhcpserver\dhcpsrv.exe > Admin
- Stop + Remove + Remove

- Stop & Start the VM > Wait until the machine gets a IP on `Default Switch`.

- Adjust DNS_0 in `C:\dhcpserver\dhcpsrv.ini` with new DHCP server IP address

- Run C:\dhcpserver\dhcpsrv.exe > Admin
- Install + Start + Configure

- Stop & Start the VM > Wait until the machine gets a IP on both switches.

- Run C:\dhcpserver\dhcpsrv.exe > Admin
- Stop + Remove + Remove

## SOLUTION 2 : Fix the IP in the VM

References:
- https://www.petri.com/configuring-vm-networking-hyper-v-nat-switch
- https://gist.github.com/foglcz/28a2a3fc00edffdb9cb3

First `start the vm` to get a IP on `Default Switch`.

Then set the second IP on `hypervnat` via powershell:
```bash
# First copy the gist function `Set-VMNetworkConfiguration` and paste it
$vmname  = "base"
$vmip    = "169.254.54.100"
$subnet  = "255.255.255.0"
$dnssrv  = "10.0.10.60","10.0.92.181","10.0.93.182"
$gateway = "169.254.54.254"
Get-VMNetworkAdapter -VMName $vmname -Name "Network Adapter" |
Set-VMNetworkConfiguration -IPAddress $vmip -Subnet $subnet -DNSServer $dnssrv -DefaultGateway $gateway
#Set-VMNetworkConfiguration -VMName $vmname -IPAddress $vmip -Subnet $subnet -DNSServer $dnssrv -DefaultGateway $gateway
```

If connecting to another physical network, re-run the same command with a different $dnssrv array value.

## SOLUTION 3 : Connect the nat network to a public network

If internet connection sharing has been disabled by the network administrator:

1. Start > Run > gpedit.msc
2. Locate;
- Computer Configuration/Administrative Templates/Network/Network Connections
3. Disable the following policies;
- Prohibit installation and configuration of Network Bridge on your DNS domain network
- Prohibit use of Internet Connection Firewall on your DNS domain network
- Prohibit use of Internet Connection Sharing on your DNS domain network
- Require domain users to elevate when setting a network’s location
4. Start > Run > regedit
5. Locate;
- Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\Network Connections
6. Add/update a registry DWORD entry for the following, and set it to 1;
- NC_PersonalFirewallConfig
- NC_ShowSharedAccessUI

Share the network connection:

1. Control Panel > Network and Sharing Center
2. Locate;
- `vEthernet (Default Switch)`
3. Right-Click > Properties > Open tab `Sharing`
- Enable `Allow other network users to connect through this computer's Internet connection`
- Select Home networking connection: `vEthernet (hypervnat)`
- Enable `Allow other network users to control or disable the shared Internet connection`
4. OK and Accept

Create internal defaults to DHCP > Turn it to manual 192.168.137.1 > Internet Connection Sharing from Wifi or Ethernet

# SOLUTION 4 : route ip

```bash
#powershell
#Create an ip alias to eth0 as 192.168.137.XXX
route ADD 192.168.137.XXX MASK 255.255.255.255 172.21.235.130
#route DELETE 192.168.137.XXX
```

# SOLUTION 5 : Setup a NAT network for Hyper-V guests

```bash
#powershell
Get-VMSwitch
New-VMSwitch –SwitchName "hypervnat" –SwitchType Internal –Verbose
Get-NetAdapter # Get ifIndex
New-NetIPAddress –IPAddress 192.168.137.1 -PrefixLength 24 -InterfaceIndex 57 –Verbose
# This step connects the Internal network to the Internet
New-NetNat –Name NATNetwork –InternalIPInterfaceAddressPrefix 192.168.137.0/24 –Verbose
Get-VM -name base | Get-VMNetworkAdapter | Connect-VMNetworkAdapter –SwitchName "hypervnat"
```

Temporary add a second network adapter on "Default Switch" to get a ip.
Connect to the VM and configure a static ip on eth0 as 192.168.137.XXX.
Stop the VM, Remove the secondary network adapter, Start the VM.
The VM should start with the static configured IP.
