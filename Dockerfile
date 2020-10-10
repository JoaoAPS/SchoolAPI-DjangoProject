FROM python:3.8-alpine
MAINTAINER João A. Paludo Silveira

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install -r /requirements.txt
RUN apk --purge del .build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
