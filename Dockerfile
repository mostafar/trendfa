FROM ubuntu:xenial

RUN apt-get update && apt-get install -y \
    python3-pip

COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt

