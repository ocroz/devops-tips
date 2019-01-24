# Setup a local dns server

https://www.digitalocean.com/community/tutorials/how-to-configure-bind-as-a-private-network-dns-server-on-centos-7

```bash
sudo yum install bind bind-utils -y
```

/etc/named.conf
```bash
# Change these 3 options to any;
# So the dns server is accessible from any other server or docker container
options {
        listen-on port 53 { any; };
        listen-on-v6 port 53 { any; };
        allow-query     { any; };
};

# Append this line at the end of file
include "/etc/named/named.conf.local";
```

/etc/named/named.conf.local
```bash
zone "localdns" {
    type master;
    file "/etc/named/zones/db.localdns"; # zone file path
};
zone "0.127.in-addr.arpa" {
    type master;
    file "/etc/named/zones/db.127.0";  # 127.0.0.0/16 subnet
};
```

/etc/named/zones/db.localdns
```bash
$TTL    604800
@       IN      SOA     ns1.localdns. admin.localdns. (
                  3       ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
; name servers - NS records
     IN      NS      ns1.localdns.

; name servers - A records
ns1.localdns.         IN      A      127.0.0.1

; 127.0.0.0/16 - A records
java.localdns.        IN      A      127.0.0.1
```

/etc/named/zones/db.127.0
```bash
$TTL    604800
@       IN      SOA     localdns. admin.localdns. (
                              3         ; Serial
                         604800         ; Refresh
                          86400         ; Retry
                        2419200         ; Expire
                         604800 )       ; Negative Cache TTL
; name servers
      IN      NS      ns1.localdns.

; PTR Records
1.0     IN      PTR     ns1.localdns.        ; 127.0.0.1
1.0     IN      PTR     java.localdns.       ; 127.0.0.1
```

```bash
# First check
sudo named-checkconf
sudo named-checkzone localdns /etc/named/zones/db.localdns
sudo named-checkzone 0.127.in-addr.arpa /etc/named/zones/db.127.0

# Then start the service
sudo systemctl start named
sudo systemctl status named
sudo systemctl enable named

# Eventually check the dns service
dig @localhost java.localdns # Should return 127.0.0.1
nslookup java.localdns       # Should return 127.0.0.1

# Add these lines into: /etc/resolv.conf
nameserver 127.0.0.1 # Remove the other lines if ping fails to resolve
search localdns

# Make these changes persistent via: /etc/sysconfig/network-scripts/ifcfg-eth0
DNS1=8.8.8.8
DNS2=8.8.4.4

# Ping should now work
nslookup java # Should return 127.0.0.1
ping java     # Should ping 127.0.0.1

# Possible other configs
sudo iptables -t nat -A INPUT -p udp -m udp --dport 53 -j ACCEPT
sudo iptables -t nat -A OUTPUT -p udp -m udp --sport 53 -j ACCEPT
```
