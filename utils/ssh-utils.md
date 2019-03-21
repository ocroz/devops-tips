# ssh-utils

Create private/public key pair:
```bash
ssh-keygen               # with passphrase
```

## UNIX-like installation

Load your identity only once:
```bash
eval $(ssh-agent -s)     # Start ssh agent for next commands
ssh-add                  # Write your passphrase only once
ssh-add -l               # List the loaded identities
```

Load the ssh-key on every login:
```bash
# .bash_profile
SSH_ENV="$HOME/.ssh/environment"

function start_agent {
    echo "Initialising new SSH agent..."
    /usr/bin/ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
    echo succeeded
    chmod 600 "${SSH_ENV}"
    . "${SSH_ENV}" > /dev/null
    /usr/bin/ssh-add;
}

# Source SSH settings, if applicable

if [ -f "${SSH_ENV}" ]; then
    . "${SSH_ENV}" > /dev/null
    #ps ${SSH_AGENT_PID} does not work under cywgin
    ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || {
        start_agent;
    }
else
    start_agent;
fi
```

No need to enter passphrase again, neither on localhost, nor on proxy, to reach target:
```bash
ssh user@remote-proxy -A # Forward identity to remote-proxy for remote-target
ssh user@remote-target   # No need to store private key on remote-proxy
ssh -t user@remote-proxy -A ssh user@remote-target -A # Same in one command
git clone git@server:space/repo.git # No need a local private key for git too
```

Kill the current ssh-agent is case of problems:
```bash
if [ -n "$SSH_AUTH_SOCK" ];then eval $(/usr/bin/ssh-agent -k);fi
```

## Using Putty's pageant for WSL

Install/Start putty's pageant and weasel-pageant:
- https://www.digitalocean.com/community/tutorials/how-to-use-pageant-to-streamline-ssh-key-authentication-with-putty
- https://github.com/vuori/weasel-pageant

Copy pageant shortcut under:<br/>
%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

$HOME/.bashrc
```bash
eval $(/mnt/c/Program\ Files/Putty/weasel-pageant-1.1/weasel-pageant -r)
```

Note: No other key should be loaded on login (see above) on remote-proxy or the ssh forward will fail.

## Using Putty's pageant for Git Bash

- https://github.com/cuviper/ssh-pageant

$HOME/.bashrc
```bash
eval $(/usr/bin/ssh-pageant -r -a "/tmp/.ssh-pageant-$USERNAME")
```
