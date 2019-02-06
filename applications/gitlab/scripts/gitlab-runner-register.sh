# https://gist.github.com/secfigo/ff5910b2965fbbea5bc96564a944e62c

sudo gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.kudelski.com/" \
  --registration-token "ydCgsiz-ZeLdsWA73fcZ" \
  --executor "docker" \
  --docker-image alpine \
  --description "docker-runner" \
  --tag-list "docker" \
  --run-untagged \
  --docker-extra-hosts "gitlab.local:10.0.1.15" \
  --docker-privileged \
  --locked "true"

sudo gitlab-runner register \
  --non-interactive \
  --url "https://gitlab.kudelski.com/" \
  --registration-token "ydCgsiz-ZeLdsWA73fcZ" \
  --executor "shell" \
  --description "shell-runner" \
  --tag-list "shell" \
  --run-untagged \
  --locked "true"
