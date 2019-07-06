FROM python:3.6.5-alpine
MAINTAINER Brian Curtich "bcurtich@gmail.com"

RUN apk update \
  && apk upgrade \
  && rm -rf /var/cache/apk/*

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/pixelarity-download.py .

WORKDIR /tmp/downloads

ENTRYPOINT [ "python", "/usr/src/app/pixelarity-download.py" ]
