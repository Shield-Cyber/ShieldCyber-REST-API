FROM python:3.11.3

RUN curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
RUN chmod +x mkcert-v*-linux-amd64
RUN cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert
RUN mkcert -install

WORKDIR /opt

COPY requirements.txt /opt
RUN pip3 install -r requirements.txt

RUN mkdir certs
RUN mkcert -cert-file ./certs/cert.pem -key-file ./certs/key.pem localhost 127.0.0.1 0.0.0.0

ENV VERSION=2.6.12

COPY . ./app

CMD uvicorn app.main:app --host 0.0.0.0 --ssl-keyfile=./certs/key.pem --ssl-certfile=./certs/cert.pem --log-config ./app/config/log.yaml