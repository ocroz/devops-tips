# Automated Nginx Reverse Proxy for Docker

References:
- http://jasonwilder.com/blog/2014/03/25/automated-nginx-reverse-proxy-for-docker/
- https://docs.docker.com/install/linux/docker-ce/centos/
- https://github.com/jwilder/nginx-proxy/issues/582

Install docker on `docker-node` machine and:
- a `nginx` container with an optional `DEFAULT_HOST`, and
- few containers with their unique `VIRTUAL_HOST`.

```bash
# ...
# Install everything until `docker-ce` +manage-docker-as-a-non-root-user
sudo apt-get install -y docker-ce
sudo groupadd docker && sudo usermod -aG docker ubuntu && exit # and ssh again

# Install automated-nginx-reverse-proxy-for-docker
docker run -d -p 80:80 -v /var/run/docker.sock:/tmp/docker.sock -t jwilder/nginx-proxy # docker run -e DEFAULT_HOST=${one-of-below VIRTUAL_HOST} ...

# Check the logs and the nginx configuration
docker images && docker ps # --all
docker logs ${container-id-80} # docker logs --follow ${container-id-80}
docker exec -it ${container-id-80} cat /etc/nginx/conf.d/default.conf

# Get a sample nodejs-starter-app
git clone https://github.com/IBM/dWTVSimpleContainerApp
cd dWTVSimpleContainerApp/

# Run VIRTUAL_HOST=start-app at localhost:6006
docker build -t start-app:v1 .
docker create start-app:v1
docker stop ${container-id-6006}
docker commit ${container-id-6006} start-app:v2
docker run -e VIRTUAL_HOST=start-app -p 6006:6006 -td start-app:v2

# Update the sample nodejs-starter-app
vi Dockerfile app.js public/index.html # Change port to 6007

# Run VIRTUAL_HOST=start-app-6007 at localhost:6007
docker build -t start-app-6007:v1 .
docker create start-app-6007:v1
docker stop ${container-id-6007}
docker commit ${container-id-6007} start-app-6007:v2
docker run -e VIRTUAL_HOST=start-app-6007 -p 6006:6006 -td start-app-6007:v2

# Check the new configuration and watch new connections
docker exec -it ${container-id-80} cat /etc/nginx/conf.d/default.conf
docker logs --follow ${container-id-80}
```

Update your hosts file with several hostnames for `docker-node` machine IP:
```bash
10.177.194.100  docker-node  start-app  start-app-6007
```

Then open the different URLs in your browser:
- http://start-app -> Render `start-app`.
- http://start-app-6007 -> Render `start-app-6007`.
- http://docker-node -> Render `start-app` if set as `DEFAULT_HOST`.
