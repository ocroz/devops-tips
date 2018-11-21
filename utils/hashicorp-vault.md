# Manage secrets with HashiCorp Vault

## Installation

```bash
curl https://releases.hashicorp.com/vault/0.11.3/vault_0.11.3_linux_amd64.zip \
    -o vault_0.11.3_linux_amd64.zip
sudo unzip vault_0.11.3_linux_amd64.zip -d /usr/bin/
rm vault*.zip
vault
vault status
```

## Start vault as a service

```bash
sudo yum install -y supervisor
sudo service supervisord start # sudo /bin/systemctl enable supervisord
```

/etc/supervisord.d/vault.ini
```bash
[program:vault]
command=vault server -dev # Run in-memory, use consul as backend for production
directory=/home/centos
user=centos
```

```bash
sudo service supervisord restart
export VAULT_ADDR='http://127.0.0.1:8200'
vault status
```

## Write, Get, and Delete secret

```bash
vault kv put secret/hello foo=world
vault kv get secret/hello
vault kv get -field=foo secret/hello
vault kv delete secret/hello
```

## vault-token-tower

See https://github.com/madchap/docker-vault-token-tower
- https://www.vaultproject.io/guides/operations/vault-ha-consul.html
- https://www.vaultproject.io/docs/concepts/policies.html
- https://learn.hashicorp.com/vault/getting-started/apis
- https://learn.hashicorp.com/vault/identity-access-management/iam-identity
- https://www.vaultproject.io/api/

Unseal the vault servers
```bash
# First time (on every vault server)
vault operator init       # Returns N unseal keys + the initial root token
vault operator unseal     # Inject n/N unseal keys
vault login ${root-token} # Get access to all the secrets
```

Manage the primary secrets
```bash
# High level operator commands
vault operator seal          # Lock vault: Need to restart the unseal process
vault operator rekey         # Generate new unseal keys
vault token revoke           # Revoke current token and its children
vault operator generate-root # Generate new root token
```

### As root (or sufficient admin user)

```bash
export VAULT_TOKEN=${root-token} # As root
```

Enable authentications
```bash
# Enable authentication: userpass or ldap, github, etc.
curl --request POST --header "X-Vault-Token: $VAULT_TOKEN" \
  --data '{"type": "userpass"}' http://127.0.0.1:8200/v1/sys/auth/userpass
# Enable authentication: AppRole
curl --request POST --header "X-Vault-Token: $VAULT_TOKEN" \
  --data '{"type": "userpass"}' http://127.0.0.1:8200/v1/sys/auth/approle
```

List and Read policies (and below to Add/Update policy)
```bash
vault policy list
vault policy read default
```

bin/hcl2str
```bash
cat $1 | sed 's,$,~,g' | tr -d '\n' | sed 's,~,\\n,g;s,",\\",g'
```

policy.hcl
```bash
path "auth/token/renew" {
 capabilities = ["update"]
}
path "secret/db/psql/jira" {
 capabilities = ["list", "read"]
}
path "secret/db/psql/jira/*" {
 capabilities = ["list", "read", "create", "update"]
}
```

Add policy
```bash
echo "{\"policy\":\"$(hcl2str policy.hcl)\"}" > payload.json
curl --request POST --header "X-Vault-Token: $VAULT_TOKEN" \
  --data @payload.json http://127.0.0.1:8200/v1/sys/policy/db-psql-jira
```

Create User with policies
```bash
curl --request POST --header "X-Vault-Token: $VAULT_TOKEN" \
  --data '{"password": "S3cr3T", "policies": ["db-admin", "..."]}' \
  http://127.0.0.1:8200/v1/auth/userpass/users/bob
```

Login and Get token
```bash
curl --request POST --data '{"password": "S3cr3T"}' \
  http://127.0.0.1:8200/v1/auth/userpass/login/bob
export VAULT_TOKEN=${user-token} # As bob
```

Create AppRole with policies
```bash
curl --request POST --header "X-Vault-Token: $VAULT_TOKEN" \
  --data '{"policies": ["db-psql-jira"]}' \
  http://127.0.0.1:8200/v1/auth/approle/role/app-jira
```

Get Role ID: Give it to the app (git it)
```bash
curl --header "X-Vault-Token: $VAULT_TOKEN" \
  http://127.0.0.1:8200/v1/auth/approle/role/app-jira/role-id
```

Create new Secret ID (as root or admin user): Store it locally (don't git it)
```bash
curl --request POST --header "X-Vault-Token: $VAULT_TOKEN" \
  http://127.0.0.1:8200/v1/auth/approle/role/app-jira/secret-id
```

Fetch new vault token (from Role ID and Secret ID)
```bash
curl --data '{"role_id": "${role_id}", "secret_id": "${secret_id}"}' \
  --request POST http://127.0.0.1:8200/v1/auth/approle/login
```

Run as new AppRole user + See/Renew client token before end of lease duration
```bash
export VAULT_TOKEN=${approle-token} # As app-jira
curl --header "X-Vault-Token: $VAULT_TOKEN" \
  http://127.0.0.1:8200/v1/auth/token/lookup-self
curl --header "X-Vault-Token: $VAULT_TOKEN" \
  --request POST --data "{\"token\": \"$VAULT_TOKEN\"}" \
  http://127.0.0.1:8200/v1/auth/token/renew
```

Access the secret: Read and Write Key/value pairs
```bash
curl --header "X-Vault-Token: $VAULT_TOKEN" --request POST \
  --data '{"bar": "baz"}' http://127.0.0.1:8200/v1/secret/db/psql/jira/foo
curl --header "X-Vault-Token: $VAULT_TOKEN" \
  http://127.0.0.1:8200/v1/secret/db/psql/jira/foo
```
