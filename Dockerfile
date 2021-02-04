FROM alpine:3.12

RUN apk update &&\
    apk --no-cache add python3 python3-dev py3-pip py3-wheel unixodbc unixodbc-dev gcc g++

RUN mkdir -p /build
COPY . /build

WORKDIR /build
RUN pip install . &&\
    pip install -r optional-requirements.txt

WORKDIR /
RUN rm -rf /build &&\
    apk --no-cache del g++ gcc unixodbc-dev py3-wheel py3-pip python3-dev &&\
    mkdir -p /data

VOLUME "/data"
ENTRYPOINT "/usr/bin/journald-monitor -c /data/config.yaml"
