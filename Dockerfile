FROM centos/python-38-centos7:latest

WORKDIR /work
COPY . .

ENV SHELL /bin/bash
ENV PIPENV_VENV_IN_PROJECT "true"

RUN pip install pipenv
RUN pipenv install -r requirements.txt