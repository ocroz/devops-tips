# Docker on openstack

```bash
sudo apt-get install -y docker-ce
sudo groupadd docker && sudo usermod -aG docker ubuntu
exit # and ssh again

git clone https://github.com/IBM/dWTVSimpleContainerApp
cd dWTVSimpleContainerApp/

docker build -t nodejs-starter-app:v1 .
docker image ls

docker create nodejs-starter-app:v1
docker ps --all

docker start 0727d5a73ed0
docker ps

docker exec -it 0727d5a73ed0 bash
docker logs 0727d5a73ed0

docker inspect 0727d5a73ed0 | grep -E "IPAddress|tcp"
docker port 0727d5a73ed0
# No result
docker port 0727d5a73ed0 6006/tcp # or 6006
# Error: No public port '6006/tcp' published for 0727d5a73ed0

docker stop 0727d5a73ed0
docker commit 0727d5a73ed0 nodejs-starter-app:v2
docker image ls

docker run -p 6006:6006 -td 5829d033d0cc
docker ps

docker inspect ba01e56842ef | grep -E "IPAddress|tcp"
docker port ba01e56842ef # 6006/tcp -> 0.0.0.0:6006
docker port ba01e56842ef 6006/tcp # 0.0.0.0:6006
curl http://172.17.0.2:6006/ # It works locally but not from browser
```

Create a `security group` in `openstack` via `Access & Security` to open port `6006` then edit the security groups of the given `instance` and select it.

Now access the application: [http://instance:port/](http://openstack:6006/).
