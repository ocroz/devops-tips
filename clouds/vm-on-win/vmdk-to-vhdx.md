# Convert a VMDK file a a VDHX file

- https://blogs.msdn.microsoft.com/timomta/2015/06/11/how-to-convert-a-vmware-vmdk-to-hyper-v-vhd/
- https://www.microsoft.com/en-us/download/confirmation.aspx?id=42497

Install the MSI then:
```bash
#powershell
Import-Module 'C:\Program Files\Microsoft Virtual Machine Converter\MvmcCmdlet.psd1'
ConvertTo-MvmcVirtualHardDisk -SourceLiteralPath 'disk.vmdk' -VhdType DynamicHardDisk -VhdFormat vhdx -destination .
```
