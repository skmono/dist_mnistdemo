#!/bin/bash

# build docker image with Tensorflow
docker build -t tfimage docker/

# generate network bridge
docker network create tfdistnetwork


