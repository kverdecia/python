# ==================================== BASE ====================================
FROM python:3.6-alpine as base

RUN adduser -D -g '' uwsgi

RUN apk update

RUN set -ex && apk --no-cache add sudo
RUN echo "set disable_coredump false" >> /etc/sudo.conf

RUN apk add curl
RUN apk add linux-headers
RUN apk add build-base
RUN apk add postgresql-libs
RUN apk add --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev python3-dev

RUN pip install --upgrade pip
RUN pip install pipenv

RUN mkdir /app
ENV PYTHONPATH $PYTHONPATH:/app

WORKDIR /app
ADD . /app
RUN chown -R uwsgi:uwsgi /app
RUN sudo -u uwsgi pipenv install

RUN apk --purge del .build-deps

ENV FLASK_APP=myapp.py


# ==================================== MANAGE ====================================
FROM base AS manage

ENTRYPOINT ["sudo", "-u", "uwsgi", "pipenv", "run", "flask"]


# ==================================== TEST ====================================
FROM base AS test

ENTRYPOINT ["sudo", "-u", "uwsgi", "pipenv", "run", "pytest"]


# ==================================== PRODUCTION ====================================
FROM base AS production

ENV PORT=5000
CMD sudo -u uwsgi pipenv run uwsgi uwsgi.ini --thunder-lock
