FROM python:3.12-bookworm

WORKDIR /app

RUN pip install --no-cache-dir gitpython requests

COPY ./.watching ./.watching
COPY ./executer ./executer
COPY ./start.sh .
COPY ./setup.py .

ENTRYPOINT ["/bin/bash", "./start.sh"]