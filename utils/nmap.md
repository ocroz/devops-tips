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

On Windows: https://superuser.com/questions/352017/pid4-using-port-80
```powershell
# RunAs Admin
netstat -aon
netstat -aon | findstr ":80"
tasklist /svc /FI "PID eq 4"
```
