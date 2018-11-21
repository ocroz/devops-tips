# Configuration for git

```bash
sudo yum install git -y
git config --global user.name "Olivier Crozier"
git config --global user.email olivier.crozier@nagra.com

curl -O https://raw.githubusercontent.com/deliciousinsights/support-files/master/config-git.sh
source ./config-git.sh

# .bashrc (if no PS1 found)
# Git completion and prompt definitions
source /etc/bash_completion.d/git
source /usr/share/git-core/contrib/completion/git-prompt.sh
```
