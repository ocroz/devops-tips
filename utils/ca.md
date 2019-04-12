# Setup your own CA with OpenSSL

References:
- https://stackoverflow.com/questions/10175812
- https://gist.github.com/Soarez/9688998
- https://jamielinux.com/docs/openssl-certificate-authority
- https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/

Modern browsers (like the warez we're using in 2014/2015) want a certificate that chains back to a trust anchor, and they want DNS names to be presented in particular ways in the certificate. And browsers are actively moving against self-signed server certificates.

Some browsers don't exactly make it easy to import a self-signed server certificate. In fact, you can't with some browsers, like Android's browser. So the complete solution is to become your own authority.

The best way to avoid this is:
1. Create your own authority (i.e., become a CA)
2. Create a certificate signing request (CSR) for the server
3. Sign the server's CSR with your CA key
4. Install the server certificate on the server
5. Install the CA certificate on the client

## Create your own authority

```bash
# ca private key and root certificate (valid for 20 years)
openssl genrsa -aes256 -out ca.key.pem 4096
openssl req -x509 -new -key ca.key.pem -sha256 -days 7300 -out ca.cert.pem
```

## Create a certificate signing request (CSR) for the server

```bash
# server key, and csr
myserver=${application}.${domain}
openssl genrsa -out $myserver.key 2048
openssl req -new -key $myserver.key -out $myserver.csr
```

## Sign the server's CSR with your CA key

$myserver.ext
```
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = ${application}
DNS.2 = ${application}.${domain}
DNS.3 = ${application}.${ip}.xip.io
```

```bash
# signed certificate with DNS names (valid for 5 years)
openssl x509 -req -in $myserver.csr -CA ca.cert.pem -CAkey ca.key.pem -CAcreateserial -days 1825 -sha256 -extfile $myserver.ext -out $myserver.crt
openssl x509 -noout -text -in $myserver.crt # verify the certificate
```

## Install the server certificate on the server

Deploy the following files on the server:
- ca.cert.pem
- $myserver.key
- $myserver.crt

## Install the CA certificate on the client

Deploy the following file on the server:
- ca.cert.pem

```bash
cp *.pem /etc/pki/ca-trust/source/anchors/
update-ca-trust extract
```

## Troubleshooting

Is the connection still insecure?
- Check the IP defined in $myserver.ext, possible do not define any IP here.
