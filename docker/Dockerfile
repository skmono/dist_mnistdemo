FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    wget \
    gcc-7 \
    g++-7 \
    python3-dev \
    python3-pip \
    python3-setuptools \
    && rm -rf /var/lib/lists/*

RUN pip3 install --upgrade pip \
    && pip install tensorflow
