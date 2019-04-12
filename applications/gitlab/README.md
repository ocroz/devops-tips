# Gitlab

- https://about.gitlab.com/solutions/
- https://about.gitlab.com/product/
- https://about.gitlab.com/services/
- https://about.gitlab.com/devops-tools/

- https://about.gitlab.com/features/
- https://about.gitlab.com/pricing/#self-managed

## Installation

- https://about.gitlab.com/install/#centos-7?version=ce
- https://gist.github.com/secfigo/ff5910b2965fbbea5bc96564a944e62c
- https://gitlab.com/gitlab-org/gitlab-ce/issues/20280

### SSL

See https://docs.gitlab.com/omnibus/settings/nginx.html#manually-configuring-https

```bash
sudo vi /etc/gitlab/gitlab.rb
> external_url 'https://gitlab.example.com/'

sudo vi /etc/gitlab/ssl/ca.crt # The trusted root certificate (if unknown)
sudo vi /etc/gitlab/ssl/gitlab.example.com.key # The key without passphrase
sudo vi /etc/gitlab/ssl/gitlab.example.com.crt # The application certificate
sudo gitlab-ctl reconfigure
```

On client: Install ca.crt as trusted root certificate (see ca.md).

Tip for docker: `sudo systemctl restart docker`.

## Runner

- https://docs.gitlab.com/runner/install/
- https://gist.github.com/secfigo/ff5910b2965fbbea5bc96564a944e62c

```bash
CI_URL=https://gitlab.example.com/
CI_TOKEN=t0k3n
CI_HOST=gitlab.example.com:35.231.145.151

# Default docker volumes:
# - To share gitlab ci cache with shell runner on same machine
# - To share ssh socket with shell runner on same machine
sudo gitlab-runner register \
  --non-interactive \
  --url "$CI_URL" \
  --registration-token "$CI_TOKEN" \
  --executor "docker" \
  --docker-image alpine \
  --docker-volumes '/home/gitlab-runner/cache:/cache' \
  --docker-volumes '/tmp:/tmp' \
  --docker-extra-hosts "$CI_HOST" \
  --docker-privileged \
  --description "docker-runner" \
  --tag-list "$(hostname -s),docker" \
  --run-untagged \
  --locked=true

sudo gitlab-runner register \
  --non-interactive \
  --url "$CI_URL" \
  --registration-token "$CI_TOKEN" \
  --executor "shell" \
  --description "shell-runner" \
  --tag-list "$(hostname -s),shell" \
  --run-untagged \
  --locked=true
```

### Troubleshooting

Gitlab might fail to pick up a runner:
```bash
# Service
sudo gitlab-runner status
sudo gitlab-runner restart # Even if Service is running!
# Runners
sudo gitlab-runner list
sudo gitlab-runner verify # [-u $url -t t0k3n]
sudo gitlab-runner unregister --all-runners # [-u $url -t t0k3n]
sudo gitlab-runner verify --delete # For runners that fail to unregister
```

## Registry

See https://docs.gitlab.com/ce/administration/container_registry.html

On Gitlab server:
```bash
$ sudo vi /etc/gitlab/gitlab.rb
registry_external_url 'https://gitlab.example.com:4567'

$ sudo gitlab-ctl reconfigure

# Then open port 4567
```

See https://docs.gitlab.com/ce/ci/variables/predefined_variables.html

On Gitlab runner:
```bash
docker login $CI_REGISTRY # gitlab.example.com:4567
IMG=img/latest
docker tag $IMG $CI_REGISTRY/$GITLAB_USER_LOGIN/$CI_PROJECT_NAME/$IMG
docker login $CI_REGISTRY -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD
docker push $CI_REGISTRY/$GITLAB_USER_LOGIN/$CI_PROJECT_NAME/$IMG
```
PS: The gitlab user $CI_DEPLOY_USER (logged by default, no need to login) has Read/Only access; it can pull, not push.

## Cache vs Artifacts

See https://docs.gitlab.com/ce/ci/caching/

The docker runner must have 2 volumes by default in order to share cache and ssh socket with host:
- /home/gitlab-runner/cache:/cache
- /tmp:/tmp # export SSH_AUTH_SOCK=/tmp/ssh-t0k3n/agent.PID

The host cache must be created before any other operation, because the host cache must be created as gitlab-runner so in a shell runner (a docker runner creates cache as root in the host).

In .gitlab-ci.yml:
- The `cache key` relates to the host cache (to share cache between runners) and it is persistent.
- The `cache paths` relates to the local cache (inside the git workspace) and it is erased when starting any job (then populated again from host cache).

```bash
cache:
  key: $CACHE_KEY
  paths:
    - $CACHE_PATH
```
