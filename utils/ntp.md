# Network Time Protocal

https://www.ntppool.org/

```bash
sudo yum install ntp -y

sudo systemctl start ntpd
sudo systemctl status ntpd
sudo systemctl enable ntpd

sudo firewall-cmd --permanent --add-service=ntp
sudo firewall-cmd --reload
```
