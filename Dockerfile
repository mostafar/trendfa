FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
    python3-pip

RUN pip3 install --upgrade pip
COPY . /src
WORKDIR /src
RUN pip3 install -r requirements.txt

