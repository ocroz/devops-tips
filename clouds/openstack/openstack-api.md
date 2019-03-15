# Use the Openstack REST API

See:
- https://developer.openstack.org/api-guide/quick-start/api-quick-start.html
- https://developer.openstack.org/api-ref/ > identity > Identity API Operations

```bash
token=$(openstack token issue | grep ' id ' | awk '{print $4}')
alias python=/usr/bin/python3; alias pyjson="python -m json.tool";

curl -X GET -H "X-Auth-Token: $token" $OS_AUTH_URL/v3/auth/projects | pyjson
curl -X GET -H "X-Auth-Token: $token" $OS_AUTH_URL/v3/auth/catalog | pyjson
```

https://developer.openstack.org/api-ref/object-store

```bash
OS_SWIFT_URL=$(curl -s -H "X-Auth-Token: $token" $OS_AUTH_URL/v3/auth/catalog | python -c 'import re,sys,json; eps=[x["endpoints"] for x in json.load(sys.stdin)["catalog"] if x["name"] == "swift"][0]; print("%s" % [x["url"] for x in eps if re.match("^https:",x["url"])][0]);');echo $OS_SWIFT_URL

publicURL=https://cloud.eu-zrh.hub.kudelski.com:8080/swift/v1

# Accounts
curl -i $publicURL -X HEAD -H "X-Auth-Token: $token"
curl -i $publicURL -X GET -H "X-Auth-Token: $token"

# Containers
curl -i $publicURL/backups/ -X GET -H "X-Auth-Token: $token"
curl -i $publicURL/backups/books/ -X PUT -H "X-Auth-Token: $token" -H "Content-Length: 0"
curl -i $publicURL/backups/books/ -X DELETE -H "X-Auth-Token: $token"

# Objects (PUT --data-binary to preserve line breaks from files)
echo "# blah blah" >save-my-work.txt
curl -i $publicURL/backups/save-my-work.txt -X PUT -d @save-my-work.txt \
    -H "Content-Type: text/html; charset=UTF-8" -H "X-Auth-Token: $token"
curl -i $publicURL/backups/save-my-work.txt -X GET -H "X-Auth-Token: $token"
echo -e "# blah blah\n# toto tata" >save-my-work.txt
curl -i $publicURL/backups/save-my-work.txt -X PUT \
    --data-binary @save-my-work.txt -H "X-Auth-Token: $token"
curl -i $publicURL/backups/save-my-work.txt -X GET -H "X-Auth-Token: $token"
```

https://developer.openstack.org/api-ref/network/v2/index.html#networks

```bash
publicURL=https://cloud.eu-zrh.hub.kudelski.com:9696
curl -i -X GET -H "X-Auth-Token: $token" $publicURL
curl -i -X GET -H "X-Auth-Token: $token" $publicURL/v2.0/networks
```
