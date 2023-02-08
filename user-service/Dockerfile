FROM alpine:3.8 AS builder

#Add bash to the image
RUN apk add --no-cache py3-pip python3 bash

COPY requirements.txt /usr/app/
WORKDIR /usr/app/
RUN pip3 install -r requirements.txt

#Add new stage
FROM builder AS finisher

COPY . /usr/app/

EXPOSE 5001

RUN chmod +x /usr/app/entrypoint.sh
ENTRYPOINT ["/usr/app/entrypoint.sh"]
