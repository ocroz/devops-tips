# Docker on openstack

References:
- https://wiki.openstack.org/wiki/Zun
- https://docs.openstack.org/zun/latest

```bash
pip install python-zunclient

sudo apt-get install -y mysql-server
sudo mysql
```

```sql
CREATE DATABASE zun;
GRANT ALL PRIVILEGES ON zun.* TO 'zun'@'localhost' \
  IDENTIFIED BY 'ZUN_DBPASS';
GRANT ALL PRIVILEGES ON zun.* TO 'zun'@'%' \
  IDENTIFIED BY 'ZUN_DBPASS';
exit
```

```bash
openstack user create --domain default --password-prompt zun
# The request you have made requires authentication. (HTTP 401)
```
