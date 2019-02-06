# Install bitwarden on premise

Installation:
- https://help.bitwarden.com/
- https://help.bitwarden.com/hosting/
- https://help.bitwarden.com/article/install-on-premise/

```bash
(!) Do you want to generate a self-signed SSL certificate? (y/n): y
```

GUI / Master Account:
- https://localhost # Use `https://${IP}` as it fails with `http`.
- https://help.bitwarden.com/article/admin-portal/

CLI:
- https://help.bitwarden.com/article/cli/
- https://github.com/bitwarden/cli/issues/9

```bash
# bash
export NODE_EXTRA_CA_CERTS=/bitwarden/bwdata/ssl/self/localhost/certificate.crt

# powershell
$crt="C:\bitwarden\bwdata\ssl\self\localhost\certificate.crt"
[Environment]::SetEnvironmentVariable("NODE_EXTRA_CA_CERTS",$crt)

# Login / Unlock
bw config server https://localhost
bw login
bw unlock

# Set the session key
export BW_SESSION="" # bash
$Env:BW_SESSION=""   # powershell

# Use the CLI
bw list items
```

Brave/Chrome browser extension:
- https://chrome.google.com/webstore/detail/bitwarden-free-password-m/nngceckbapebfimnlniiiahkandclblb/related

Sources:
- https://github.com/bitwarden
- https://github.com/bitwarden/server

API / Fork project:
- https://directory.fsf.org/wiki/Bitwarden-ruby
- https://github.com/jcs/rubywarden
- https://github.com/jcs/rubywarden/blob/master/API.md
