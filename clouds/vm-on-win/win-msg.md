# Send message to a user on a remote computer on Windows

You need the login credentials to send the msg on the remote computer.

## Add the credential for User on remote ComputerName

Control Panel > Credential Manager > Windows Credentials >
Add a Windows credential:
- IP or ComputerName
- Username
- Password

## Send message

```
msg /SERVER:$ComputerName $User /TIME:30 Your message!!!
```
