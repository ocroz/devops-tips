# Install helix via saltstack

See https://www.perforce.com/perforce-packages

```bash
sudo rpm --import https://package.perforce.com/perforce.pubkey
sudo vi /etc/yum.repos.d/perforce.repo
```

```text
[perforce]
name=Perforce
baseurl=http://package.perforce.com/yum/rhel/{version}/x86_64
enabled=1
gpgcheck=1
```

```bash
sudo salt p4* cmd.run 'rpm --import https://package.perforce.com/perforce.pubkey'
```

/srv/salt/top.sls
```yaml
base:
  'p4-git-tst.*':
    - helix-p4d-package
    - perforce-files
```

/srv/salt/perforce-files.sls
```yaml
perforce-user:
  user.present:
    - name: perforce
    - home: /perforce

git-client-package:
  pkg.installed:
    - name: git

perforce-source:
  git.latest:
    - name: https://github.com/ocroz/jira-node-oauth
    - rev: master
    - target: /perforce/jira-node-oauth

perforce-npm-install:
  cmd.wait:
    - name: npm install
    - cwd: /perforce/jira-node-oauth
    - watch:
      - git: perforce-source
      # - cmd: perforce-npm-install # several states can watch the same other state: they are then executed in the order seen in the sls file
```
