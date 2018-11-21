FROM alpine

MAINTAINER ocroz <olivier.crozier@gmail.com>

RUN apk update && \
    apk add util-linux && \
    rm -rf /var/cache/apk/*

ENTRYPOINT ["nsenter", "--target", "1", "--mount", "--uts", "--ipc", "--net", "--pid"]

# docker build -t hostenter .
# docker run -it --rm --privileged --pid=host hostenter
