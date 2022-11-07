FROM centos/python-38-centos7:latest

WORKDIR /work
COPY . .

RUN pip install -r requirements.txt

ENV SHELL /bin/bash

