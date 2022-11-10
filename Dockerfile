FROM apache/beam_python3.7_sdk

WORKDIR /work
COPY . .

ENV SHELL /bin/bash
ENV PIPENV_VENV_IN_PROJECT 1

RUN pip install pipenv
# RUN pipenv install -r requirements.txt