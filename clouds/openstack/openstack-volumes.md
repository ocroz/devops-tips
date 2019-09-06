# Add more disk spaces to the machines

In openstack:
- Create a volume:
  - Volume Source: No source, empty volume
  - Type: volumes_ceph
  - Size: 50GB
  - Avalability Zone: nova
- Manage Attachments: Attach it to instance.

http://www.darwinbiler.com/openstack-creating-and-attaching-a-volume-into-an-instance/
```bash
# As root
fdisk -l        # Locate the new disk /dev/vdX
fdisk /dev/vdb  # To format the new disk /dev/vdX
> n p 1 enter*2 # To create new disk partition...
> t 83          # ...of type linux
> p w           # Check (device boot should be /dev/vdX1) and Write
```

```bash
mount | grep vdb && \
  umount -l /dev/vdb  # umount if mounted
mkfs.ext4 /dev/vdb1   # Create the filesystem
```

https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/2/html/Getting_Started_Guide/ch16s03.html
```bash
sudo blkid # See the UUID of the volumes attached to the machine
ls /dev/disk/by-uuid/ # Idem
```

https://serverfault.com/questions/138555/setup-symbolic-link-where-users-can-access-it-with-ftp
```bash
mkdir -p /mnt/${volume}
mount /dev/disk/by-uuid/${uuid} /mnt/${volume} # mount /dev/vdb1 /mnt/${volume}

# Either symlink
ln -s /mnt/${volume}/${repo} /var/ftp/${repo}

# Or mount + setsebool
mkdir /var/ftp/${repo}
mount --bind /mnt/${volume}/${repo} /var/ftp/${repo}
setsebool -P ftpd_full_access=on
```

Keep the mount at reboot
```bash
echo "/dev/vdb1 /mnt/${volume} ext4 defaults 0 0">>/etc/fstab
```
