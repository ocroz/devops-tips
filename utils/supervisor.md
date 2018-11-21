# start command as a daemon with supervisor

Or use systemd unit file?

```bash
sudo yum install -y epel-release supervisor
sudo service supervisord start && sudo /bin/systemctl enable supervisord
```

/etc/supervisord.d/command.ini
```bash
[program:command]
command=command parameters
directory=/home/user
user=user
```

```bash
sudo service supervisord restart
```
