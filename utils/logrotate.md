# Rotate log files on frequency and/or file size limit

```bash
sudo yum install -y logrotate
sudo vi /etc/logrotate.conf # include /etc/logrotate.d
```

/etc/logrotate.d/service
```bash
/var/log/service/* {
    weekly
    rotate 5
    maxage 60
    maxsize 50M
    missingok
    notifempty
    nocreate
    dateext
    compress
    olddir /var/log/service/old
}
```

By default, the installation of logrotate creates a crontab file
inside `/etc/cron.daily` named `logrotate`.
