# start command as a daemon with systemd

/etc/systemd/system/sample.service
```bash
[Unit]
Description=Description for sample script goes here
After=network.target
#Requires=network-online.target
#After=network-online.target

[Service]
#User=centos
#Group=centos
#Type=simple
#WorkingDirectory=/var/tmp
#ExecStartPre=/var/tmp/sample_init.sh
ExecStart=/var/tmp/sample_script.sh
ExecStop=/bin/kill -TERM $MAINPID
#TimeoutStartSec=0

[Install]
WantedBy=default.target
#WantedBy=multi-user.target
```

```bash
sudo systemctl start|stop|status|restart
sudo systemctl enable|disable
sudo journalctl -xe
sudo journalctl -u sample
```
