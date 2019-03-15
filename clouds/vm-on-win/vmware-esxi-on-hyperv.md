# Install VMware ESXi on Hyper-V on Windows 10

## Installation

Reference:
- https://dscottraynsford.wordpress.com/2016/04/22/install-a-vmware-esxi-6-0-hypervisor-in-a-hyper-v-vm/

Other references:
- https://thesolving.com/virtualization/install-vmware-esxi-hyper-v/
- https://rlevchenko.com/2018/01/11/how-to-customize-a-vmware-esxi-image-and-install-it-in-a-hyper-v-vm/
- https://buildvirtual.net/working-with-the-esxi-firewall/
- https://docs.trendmicro.com/all/ent/dda/v2.95/en-us/dda_2.95_olh/deploy_ch_intro.html

## Problems and Solutions

Problem: "ESX install stops on error at: nfs41client failed to load"<br/>
Solution: Install ESXI 5.5 because ESX 6+ requires a 10/100/1000 network adapter (then install the patch for ESXi 6.0 Update 1a - see below)

Problem: "Keyboard not capturing inside the hyper-v VM, while installing guest OS"<br/>
Solution: Use the native laptop keyboard

Problem: "Cannot ping the ESX guest machine from the Windows host"<br/>
Solution:
- Connect the ESX guest machine with the Ethernet connection.
- Connect the Windows host to the Internet via both the Ethernet and Wifi connections.
- route add -p ${esx-ip} MASK 255.255.255.255 ${wifi-gateway-ip} Metric 1
- See the resulted route with: tracert ${esx-ip} # traceroute ${esx-ip}

Problem: "Network errors: watchdog timeout occured for uplink vmnic0"<br/>
Solution: Install the patch for ESXi 6.0 Update 1a
- https://vnetwise.wordpress.com/2015/10/07/fighting-esxi-6-0-network-disconnectsmight-be-kb2124669/
- https://www.virten.net/2015/10/esxi-6-0-october-2015-netdev-watchdog-patch-build-3073146/
- https://kb.vmware.com/s/article/2132152 > download
- ssh$ esxcli software vib install -d $(pwd)/ESXi600-201510001.zip
- https://pubs.vmware.com/vsphere-50/index.jsp?topic=%2Fcom.vmware.vcli.ref.doc_50%2Fesxcli_network.html
- See also: https://kb.vmware.com/s/article/1017253

Problem: "VMware ESX and Hyper-V are not compatible. Remove the Hyper-V role from the system before running VMware ESX"<br/>
Solution: https://kb.vmware.com/s/article/2108724

${vmware-vm}.vmx
```
vmx.allowNested = "TRUE"
smc.version = "0"
```

Problem: "Guest machine uses a lot of CPU"<br/>
Solution: Increase the memory to prevent swaping: 8.0G + 2 CPU (2 cores).

Problem: "Unable to use mouse cursor within a virtual machine console through the vSphere Web Client on Mac OS X"<br/>
Solution: https://kb.vmware.com/s/article/2076794
