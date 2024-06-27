# pull official base image
FROM python:3.11.9-alpine3.20

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add gcc python3-dev musl-dev zlib-dev jpeg-dev mariadb-dev

COPY . .
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dreamseekers.wsgi:application"]
# EXPOSE 8000