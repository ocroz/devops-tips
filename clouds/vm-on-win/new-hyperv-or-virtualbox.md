# Install a Linux VM on Windows

## Network configuration

[Optional] Setup DockerNAT and nat again:<br/>
https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/user-guide/setup-nat-network

```powershell
Get-NetNat; Get-NetAdapter | Format-Table; Get-VMSwitch | Format-Table; Get-ContainerNetwork | Format-Table; Get-VMNetworkAdapterVlan;
```

## Create a new VM

### Add another VM in Hyper-V

On Windows Enterprise editions

STEP1: Create a new External Network Switch.
- Hyper-V > `Virtual Switch Manager` > Select `External` then `Create Virtual Switch`.
- Select the virtual network AND +disable+ `virtual LAN identification for management operating system`.

STEP2: **REBOOT Windows 10** to apply the new network settings.

STEP3: Configure the VM to use the new External Network Switch.

Hyper-V > Select the VM > Select `Settings`:
- `Security` > +disable+ `Secure Boot`.
- `Network Adapter` > Select the new virtual switch.

### Add another VM in VirtualBox

On Windows Familly Home editions (where Hyper-V is not provided)

- [Download](https://www.virtualbox.org/wiki/Downloads), Install and Start VirtualBox.
- Create New VM of type Linux in version Red Hat (64-bits).
- Adjust the memory eg 1024MB.
- Create a virtual disk now: VDI, dynamic size, adjust the size eg 30MB.

Configure VM:
- General > Advanced > clipboard AND drag & drop bidirectional.
- System > Processor > 2 CPUs.
- Storage > [Controller: IDE] Empty > Optical Drive > Select Optical Drive > Browse and select the Centos 7 ISO file.
- Network > Bridge Adapter.

## Linux VM installation

VM configuration:

CentOS 7 installation:

See https://www.tenforums.com/tutorials/2291-hyper-v-vm-install-centos-linux-windows-10-a.html
- Timezone and keyboard
- Network and localhost
- Minimal installation
- Default disk partitionning
- User root and user xxxx as non-administrator
- Reboot
- Activate network: https://lintut.com/how-to-setup-network-after-rhelcentos-7-minimal-installation/
