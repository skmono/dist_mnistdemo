#!/bin/bash

# build docker image with Tensorflow
docker build -t sk_tfimage docker/

# generate network bridge
docker network create sk_tfdistnetwork


