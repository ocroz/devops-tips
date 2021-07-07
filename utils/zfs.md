# Zeta File System

References:
- https://github.com/zfsonlinux/zfs/wiki/RHEL-and-CentOS

## Physical and Virtual disks (LVM)

```bash
# As root
fdisk -l             # Show all devices
lsblk                # Hierarchy of devices
df -hT               # Display file system type too (like lsblk -fs)
mount | column -t    # Make it readable

lvm
lvm> pvs             # Physical disks
lvm> vgs             # Virtual group
lvm> lvs             # Logical disks accessible at /dev/${VG_pool}/${LV_disk}
```

## Install/Update ZFS

```bash
# As root

# First install zfs
yum install -y http://download.zfsonlinux.org/epel/zfs-release.el7_7.noarch.rpm
yum install -y https://zfsonlinux.org/epel/zfs-release.el8_3.noarch.rpm
gpg --quiet --with-fingerprint /etc/pki/rpm-gpg/RPM-GPG-KEY-zfsonlinux
vi /etc/yum.repos.d/zfs.repo
> disable [zfs] and enable [zfs-kmod]
yum install -y zfs

# Update kernel
yum install -y yum-utils
package-cleanup -y --oldkernels --count=2
vi /etc/yum.conf      # To make it permanent
> installonly_limit=2

yum update -y kernel  # yum update -y kernel-3.10.0
reboot                                      # apply the new kernel
uname -r ; yum list installed | grep kernel # running vs installed kernel versions

# Update zfs at every Linux kernel upgrade 7.x -> 7.y or 8.z
yum remove -y zfs \
    zfs-kmod spl spl-kmod libzfs2 libnvpair1 libuutil1 libzpool2 zfs-release
yum install -y http://download.zfsonlinux.org/epel/zfs-release.el7_7.noarch.rpm
mv -f /etc/yum.repos.d/zfs.repo.rpmsave /etc/yum.repos.d/zfs.repo
yum autoremove -y
yum clean metadata
yum install -y zfs
```

## ZFS pool and datasets

```bash
# As root
which zpool zfs ; zpool version ; zfs version
/sbin/modprobe zfs

man zpool zfs

pool=data
vdev=sdb    # check with "fdisk -l" or "lsblk"

# Create pool
zpool create -m /path/to/data $pool $vdev

# zpool status
zpool list -v
zpool status -iDtvx
ZPOOL_SCRIPTS_AS_ROOT=1 zpool status -c vendor,model,size
ZPOOL_SCRIPTS_AS_ROOT=1 zpool iostat -vc slaves

# zpool properties
zpool upgrade # -v | -a
zpool get all    # zpool get ashift,autoexpand,feature@lz4_compress
zpool get ashift # must be coherent with logical/physical disk sector sizes: fdisk -l
zpool get autoexpand           # should be on
zpool get feature@lz4_compress # must be active

zpool set autoexpand=on $pool
zpool set feature@lz4_compress=enabled $pool

# expand disk size, then: notify the system and expand pool
/sbin/partprobe # -s
# zpool online -e $pool $vdev # done automatically when autoexpand=on

# zfs properties
zfs get all # zfs get -s local all
zfs set compression=lz4 $pool
zfs set atime=off $pool

# Create file systems
zfs create -o mountpoint=/path/to/data1 $pool/data1
...
zfs create -o mountpoint=/path/to/dataN $pool/dataN

zfs create -o mountpoint=/path/to/data/received $pool/received
zfs unmount $pool/received && rmdir /path/to/data/received

zfs get all | grep -E "compression| atime"

# zfs status
zfs list # df -hT
zfs get compressratio $pool

# Reservations and Quotas
zfs set reservation=2M $pool/data1
zfs set quota=5M $pool/data1
...
zfs set reservation=5G $pool/dataN
zfs set quota=20G $pool/dataN
zfs get all | grep -E " reservation| quota"

# zfs permissions: Keep defaults (see https://github.com/openzfs/zfs/releases/tag/zfs-0.7.0)
# Non-privileged users are allowed to run zpool list, zpool iostat, zpool status, zpool get,
# zfs list, and zfs get. These commands no longer need to be added to the /etc/sudoers file.
```

## ZFS snapshot and send/receive to remote host

```bash
# Get latest bookmark in zpool
zpool=data
ds=${zpool}/data1
bookmark=$(zfs list -d2 ${zpool} -t bookmark -o name -s createtxg 2>/dev/null \
| tail -1 | cut -d'#' -f2)

# Take new snapshot
sudo zfs snapshot ${ds}@${snapshot}

# Send snapshot increment since last bookmark
remote_host=dns-alias-or-ip
target_ds=${zpool}/received
#sudo zfs send ${ds}@${snapshot} |
#ssh ${remote_host} sudo /usr/sbin/zfs receive -dvu ${target_ds}
sudo zfs send -i ${ds}#${bookmark} ${ds}@${snapshot} |
ssh ${remote_host} sudo /usr/sbin/zfs receive -Fdvu ${target_ds}

# Bookmark new snapshot for nest round, then destroy it
sudo zfs bookmark ${ds}@${snapshot} ${ds}#${snapshot}
sudo zfs destroy ${ds}@${snapshot}

# Destroy older snapshots (on remote)
for ds in $(zfs list -d1 ${zpool}/received -o name | grep '/.*/');do
  for snapshot in $(zfs list -d1 ${ds} -t snapshot -o name -s createtxg 2>/dev/null | grep '@' | head -n -${KEEP_OLD_SNAPSHOTS});do
    sudo zfs destroy -v $snapshot
  done
done

# Destroy older bookmarks (on local)
for ds in $(zfs list -d1 "${zpool}" -o name | grep '/');do
  for bookmark in $(zfs list -d1 ${ds} -t bookmark -o name -s createtxg 2>/dev/null | grep '#' | head -n -${KEEP_OLD_SNAPSHOTS});do
    sudo zfs destroy -v $bookmark
  done
done
```

## ZFS restore from backup

```bash
zpool=data
backup=received

# Get latest received snapshot, not necessarily yesterday
#snapshot=$(date -d yesterday +"%b%d")
snapshot=$(sudo zfs list -d2 ${zpool}/${backup} -t snapshot -o name -s createtxg | tail -1 | cut -d'@' -f2)

set -e
trap "echo -e '\nERROR> ZFS restore failed!';" ERR

for backup_ds in $(zfs list -d1 ${zpool}/${backup} -o name | grep '/.*/');do
  target_ds=$(echo ${backup_ds} | sed "s,/${backup},,g")
  sudo zfs send ${backup_ds}@${snapshot} | sudo zfs receive -Fv ${target_ds}
  sudo zfs rollback ${target_ds}@${snapshot}
  sudo zfs destroy ${target_ds}@${snapshot}
done
```
