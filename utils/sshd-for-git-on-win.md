# Configure sshd on Windows 10 for Git

## sshd

References:
- https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview

Windows Settings > Apps > Manage Optional Features
- OpenSSH Client > Install (if not done already)
- OpenSSH Server > ??

Control Panel > Administrative Tools > Services
- OpenSSH SSH Server > Start
```bash
# powershell
Start-Service sshd
```

To use key based, rather than password based, authentication:
```bash
# powershell
Install-Module -Force OpenSSHUtils -Scope AllUsers
```

Fix permission on `%USERPROFILE%\.ssh\authorized_keys`:
- Windows Explorer > Right click on the file > Properties
- Tab Security > Advanced > Disable Inheritance (first choice), then
- Both `SYSTEM` and `$domain\$user` (or email) with Full Control access
- `NT Service\sshd` with Read/Only access

Control Panel > Windows Defender Firewall > Advanced Settings > Inbound Rules
```bash
# powershell
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH SSH Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
```

Files:
- Executables are under: C:\WINDOWS\System32\OpenSSH
- Config files and logs: C:\ProgramData\ssh (sshd_config)

Configure the SSH Shell:
```bash
#powershell

# $SHELL="C:\Windows\System32\cmd.exe" # default
$SHELL="C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
# $SHELL='"C:\Program Files\Git\bin\bash.exe" --login' # gitbash
# $SHELL="C:\Windows\System32\bash.exe" # bash

New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -PropertyType String -Name DefaultShell -Value "$SHELL" -Force
```

User environment variable PATH:
- C:\Program Files\Git\bin
- C:\Program Files\Git\mingw64\bin

From any Linux:
```bash
ssh $user@$domain@$host # Should log with public key
```

Disable login with password in `C:\ProgramData\ssh\sshd_config`:
```bash
StrictModes no
PasswordAuthentication no
PubkeyAuthentication yes
```

Next:
- Allow only from user@host # or ip

## git

```bash
host="PCx" # or ip
user="userx"; domain="domx"; repo="repox"; remote=$host

git remote add $remote $user@$domain@$host:C:/Users/$user/git/$repo/.git

git config --local remote.${remote}.receivepack "powershell git receive-pack"
git config --local remote.${remote}.uploadpack "powershell git upload-pack"

git fetch $remote
git checkout $remote/master
git branch --all
```

## quick start and stop

Because it is better to keep it started as short as possible

```bash
# powershell

# START
Start-Service sshd
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH SSH Server' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
Install-Module -Force OpenSSHUtils -Scope AllUsers

# STOP
Stop-Service sshd ; Remove-NetFirewallRule -Name sshd
```
