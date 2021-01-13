#!/bin/bash

#git clone https://github.com/ziabs/url-urlshortener.git
#cd url-urlshortener

docker build -t "urlshort:1" -f docker/DockerFile .
docker network create urlshortz
docker run -d --name "rdb" --network urlshortz -p 6379:6379 redis
docker run -d --name "app" --network urlshortz -p 80:80 urlshort:1