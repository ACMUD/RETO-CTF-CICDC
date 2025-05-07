FROM python:3.12-bookworm

WORKDIR /app

RUN apt-get update
RUN apt-get install -y openssh-server

RUN mkdir /home/dev
RUN useradd -m -d /home/dev -s /bin/bash dev
RUN chown -R dev:dev /home/dev
RUN echo dev:dev123 | chpasswd

RUN pip install --no-cache-dir gitpython requests

COPY ./.watching ./.watching
COPY ./executer ./executer
COPY ./start.sh .
COPY ./setup.py .
COPY ./flag .

RUN mv ./executer/git ./executer/.git
RUN mv ./.watching/git ./.watching/.git

RUN chmod 700 /app


RUN mkdir -p /run/sshd
RUN chmod 755 /run/sshd

EXPOSE 22

ENTRYPOINT ["/bin/bash", "./start.sh"]