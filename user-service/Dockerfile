FROM alpine:3.8

RUN apk add --no-cache py3-pip python3

COPY . /usr/src/backend
RUN pip3 install -r /usr/src/backend/requirements.txt

WORKDIR /usr/src/backend

CMD python3 user.py
