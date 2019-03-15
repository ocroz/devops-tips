# VMware: Clone a VM

## Create the source VM

VMware Player > Create a New Virtual Machine
- I will install the operating system later > Next
- Guest OS & Version > Next
- Location `C:\Users\Public\Documents\VMware\Virtual Machines\${vmname}` > Next
- Store virtual disk as a single file > Next

Customize Hardware...
- Memory 2GB
- 2 Processors & tick `Virtualize Intel VT-x/EPT or AMD-V/RVI` on
- New CD/DVD (SATA) > Use ISO image file

Close and Finish

### Linux VM installation

...

### Install VMware guest addition tools (if the guest has a GUI)

Shutdown, New CD/DVD (SATA) > Use physical drive `Auto detect`
Restart the VM, Install VMware guest addition tools

Other configurations:
- hostname, disk name, screen saver, public key.

## Clone the VM

Shutdown the base VM, then...

Copy the root vm directory as a new folder:
- `C:\Users\Public\Documents\VMware\Virtual Machines\${new-name}`
- Rename the files `${vmname}.*` as `${new-name}.*`
- Replace `${vmname}.*` as `${new-name}.*` in the vmx file
- Change the location too

VMware Player > Open a Virtual Machine
- Select `I copied it`

When started:
- Change the hostname, diskname
