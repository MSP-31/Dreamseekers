# pull official base image
FROM python:3.11.9-alpine3.20

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add gcc python3-dev musl-dev zlib-dev jpeg-dev mariadb-dev

COPY . /usr/src/app/
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# 이 문장은 컨테이너가 실행될 때 기본으로 실행할 명령을 지정합니다. WORKDIR에서 지정한 디렉터리에서 실행되는 문장입니다. 

EXPOSE 8000
# 기본 포트번호는 8000입니다.