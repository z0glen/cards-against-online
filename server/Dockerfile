# pull official base image
FROM python:3.8.1-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apk update

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN \
  apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
  python3 -m pip install -r requirements.txt --no-cache-dir && \
  apk --purge del .build-deps

# copy project
COPY . /usr/src/app/

# start the application
CMD gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT run:app --access-logfile '-' --error-logfile '-' --capture-output --log-level debug