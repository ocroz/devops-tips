# Transfer files between Win10 host and Centos guest machines via a vhdx

References:
- https://www.altaro.com/hyper-v/transfer-files-linux-hyper-v-guest/
- https://docs.microsoft.com/en-us/powershell/module/hyper-v/mount-vhd
- https://superuser.com/questions/79813

## Hyper-V

Machine > Turn Off..., then
Machine > Settings... > SCSI Controller > Select "Hard Drive" > Add
- VHD: `C:\Users\Public\Documents\Hyper-V\Virtual hard disks\transfer.vhdx`
Apply changes
Machine > Start

## CentOS 7

```bash
# As root
fdisk -l        # Locate the new disk /dev/sdX
fdisk /dev/sdX  # To format the new disk /dev/sdX
> n p 1 enter*2 # To create new disk partition...
> t b           # ...of type FAT32
> p w           # Check (device boot should be /dev/sdX1) and Write
```

```bash
mkfs.vfat -n transfer /dev/sdX1   # Create the filesystem
```

```bash
mkdir /mnt/transfer
mount -t vfat /dev/sdX1 /mnt/transfer -o rw,uid=xxx,gid=xxx # Writable by user
```

## Windows 10 host

First turn off the hyper-v vm or disconnect the VDH file, then...

```powershell
$vhdx = "C:\Users\Public\Documents\Hyper-V\Virtual hard disks\transfer.vhdx"
Mount-VHD -Path "$vhdx"
```

A new drive appears in Windows Explorer.

```powershell
Get-VHD -Path "$vhdx" # Locate the DiskNumber
Dismount-VHD -DiskNumber 1
```

Then start the hyper-v vm or connect the VDH file again.
