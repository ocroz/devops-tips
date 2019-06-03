# nginx

For a secure nginx: https://cipherli.st/

```bash
sudo yum install epel-release -y
sudo yum install nginx -y
sudo service nginx start && sudo systemctl enable nginx
sudo setsebool -P httpd_can_network_connect true # Or 502 Bad Gateway
```

/etc/nginx/nginx.conf:
```
user nginx;

events {}

http {
    upstream backend {
        server localhost:port;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://backend;
        }
    }
}
```

Or /etc/nginx/conf.d/${backend}.conf
```
upstream backend {
    server localhost:port;
}
```

With /etc/nginx/default.d/${backend}.conf
```
location / {
    proxy_pass http://backend;
}
```

```bash
sudo nginx -tc /etc/nginx/nginx.conf
sudo service nginx restart
```
