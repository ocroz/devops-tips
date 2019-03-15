# Create VMware VM on Windows 10

Installation from scratch:
- https://plus.google.com/+SysAdminsHowtos/posts/6e98eRghsw1
- https://techsviewer.com/install-macos-high-sierra-vmware-windows-pc/
- https://www.sysnettechsolutions.com/en?s=mac
- https://www.sysnettechsolutions.com/en/post-sitemap.xml

VMware unlocker for MacOS:
- https://github.com/DrDonk > unlocker or esxi-unlocker
- https://www.insanelymac.com/forum/files/file/339-unlocker/

Mac on ESXi:
- https://calvin.me/install-macos-esxi/
- https://ithinkvirtual.com/2017/02/12/create-macos-os-x-vm-on-vmware-esxi-6-5-vmware-workstation-12-x/

Downgrade a macbook or macmini to its original OS version:
- https://www.imore.com/how-downgrade-macos

Mac on VMware > Edit ${vmware-vm}.vmx:
```bash
smc.version = "0"
```

Mac on VirtualBox:
```bash
# powershell
$Env:PATH = "$Env:PATH;C:\Program Files\Oracle\VirtualBox"

VBoxManage.exe modifyvm "VM Name" --cpuidset 00000001 000106e5 00100800 0098e3fd bfebfbff
VBoxManage setextradata "VM Name" "VBoxInternal/Devices/efi/0/Config/DmiSystemProduct" "iMac11,3"
VBoxManage setextradata "VM Name" "VBoxInternal/Devices/efi/0/Config/DmiSystemVersion" "1.0"
VBoxManage setextradata "VM Name" "VBoxInternal/Devices/efi/0/Config/DmiBoardProduct" "Iloveapple"
VBoxManage setextradata "VM Name" "VBoxInternal/Devices/smc/0/Config/DeviceKey" "ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc"
VBoxManage setextradata "VM Name" "VBoxInternal/Devices/smc/0/Config/GetKeyFromRealSMC" 1
```
