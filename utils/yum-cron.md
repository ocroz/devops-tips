# Configure automatic updates with yum-cron

## Configure daily security updates

```bash
sudo yum install -y yum-cron
sudo vi /etc/yum/yum-cron.conf
---
[commands]
update_cmd = security
update_messages = yes
download_updates = yes
apply_updates = yes
[emitters]
emit_via = stdio                  # email
[email]
email_from = root@localhost
email_to = root                   # olivier.crozier@nagra.com
[base]
exclude = kernel* redhat-release* # Skip updates on Linux kernel
---
sudo systemctl start yum-cron
sudo systemctl enable yum-cron
```

By default, the configuration of the yum-cron service is done through two files following exactly the same syntax:
- `/etc/yum/yum-cron.conf` defines what is done once every day,
- `/etc/yum/yum-cron-hourly.conf` defines what is done once every hour.

Still by default, no action in defined in the `/etc/yum/yum-cron-hourly.conf` file. Conversely, in the `/etc/yum/yum-cron.conf` file associated with daily actions, instructions are given to send a message on `stdio` (which means written into the `/var/log/cron` file) when any update is available (see update categories below), to download it without applying it.

```bash
[commands]
#  What kind of update to use:
# default                            = yum upgrade
# security                           = yum --security upgrade
# security-severity:Critical         = yum --sec-severity=Critical upgrade
# minimal                            = yum --bugfix update-minimal
# minimal-security                   = yum --security update-minimal
# minimal-security-severity:Critical =  --sec-severity=Critical update-minimal
```

## yum-cron and crond

```bash
systemctl status yum-cron
systemctl status crond
ls /etc/cron.* # deny, hourly, daily, weekly, monthly
```
