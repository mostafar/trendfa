FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
    python3-pip \
    locales-all

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN pip3 install --upgrade pip
COPY . /src
WORKDIR /src
RUN pip3 install -r requirements.txt
