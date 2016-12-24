#!/usr/bin/env sh

set -ex

REPO="funkyfuture/rpi-radicale"
TAG=$(grep RADICALE_VERSION= Dockerfile | cut -d "=" -f 2)

docker pull $(head -n1 Dockerfile | cut -f 2 -d " ")
docker build -t $REPO:$TAG .
