# Open ports on CentOS 7

## firewalld

```bash
sudo systemctl status iptables firewalld # Only firewalld should be running
sudo firewall-cmd --state                # Should be running
```

```bash
sudo firewall-cmd --get-default-zone # --get-active-zones | --get-zones
sudo firewall-cmd --list-all         # --list-services | --list-ports [--zone=public] [--permanent]
#sudo firewall-cmd --zone=home --change-interface=eth0
#sudo firewall-cmd --set-default-zone=home
#sudo firewall-cmd --get-services
```

```bash
sudo firewall-cmd --add-service=http    # [--zone=public] [--permanent]
sudo firewall-cmd --remove-service=http # [--zone=public] [--permanent]
```

```bash
sudo firewall-cmd --add-port=8080/tcp      # /udp [--zone=public] [--permanent]
sudo firewall-cmd --add-port=8080-8081/tcp # /udp [--zone=public] [--permanent]
```

```bash
sudo firewall-cmd --reload
```

See also https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-using-firewalld-on-centos-7

-> Creating Your Own Zones such as:

- Create zone publicweb on eth0 with services ssh http https
- Create zone privateDNS on eth1 with services dns

Then make publicweb as default zone and:

```bash
sudo systemctl restart network
sudo systemctl reload firewalld
```

## iptables

```bash
# Same command with -D to remove the rule
iptables -I INPUT -m state --state NEW -m tcp -p tcp --dport 8140 -j ACCEPT
iptables -A INPUT -m state --state NEW -m tcp -p tcp --match multiport --dports 20000:25000 -j ACCEPT
service iptables save
iptables -S # Show all the rules at once
```

## netstat and lsof

```bash
# Run with sudo to get more info
sudo netstat -pan    # ALL
sudo netstat -pantu  # tcp/udp only
sudo netstat -pantue # Extended
sudo netstat -taupen # same
sudo netstat -plntue # LISTEN only
sudo lsof -iTCP -sTCP:LISTEN -P
```
