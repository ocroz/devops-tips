# Security Enhancement Linux

```bash
# As root
sestatus
setenforce 0 # SELinux is disabled (until next reboot)

ls -lhZ # Show selinux attributes

restorecon -Rv ~/.ssh
chcon -R unconfined_u:object_r:ssh_home_t:s0 ~/.ssh
```
