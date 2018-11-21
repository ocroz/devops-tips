# Run nginx in docker

```bash
docker build -t nginx-on-java:v1 .
docker create nginx-on-java:v1
docker run -e VIRTUAL_HOST=java -p 8081:80 -td nginx-on-java:v1
```
