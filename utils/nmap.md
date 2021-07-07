# Network discovery with nmap

```bash
# As root
nmap -sP 192.168.0.0/24 # Find other devices with IPs 192.168.0.X
nmap [-O] 192.168.0.X   # Find opened ports on host with IP 192.168.0.X
nc -zv 192.168.0.X PP   # Check if port PP on 192.168.0.X is reachable
netstat -pluten         # -peanut
lsof -i :PP
socklist
```
