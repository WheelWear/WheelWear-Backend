# Alpine Linux 3.13에서 Python 3.9 이미지를 기반
FROM python:3.7-alpine3.13
WORKDIR /usr/src/app


# 이미지를 생성한 사람의 정보를 포함하는 레이블을 추가
LABEL maintainer="jonghyeon"

# pillow를 설치하기 위한 패키지 설치
RUN apk add --no-cache zlib-dev jpeg-dev gcc musl-dev

## Install packages
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

## Copy all src files
COPY . .

## Run the application on the port 8080
EXPOSE 8000

# gunicorn 배포 명령어 및 migrate
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]


# 기본적으로 컨테이너 생성시 루트 계정을 사용한다
# 보안적으로 좋지 않으므로 일반계정을 생성 후 사용용
# RUN useradd -m django-user
# USER django-user

# 도커 이미지 생성
# docker build -t backend:v1.0 .

# 도커 실행 ( --restart always)
# docker run --env-file .env/docker.env --env-file .env/django.env -itd -p 8000:8000 -v "C:\Users\009\Desktop\SK Fly AI\포폴\backend":/usr/src/app/ --name backend backend:v1.0

# 도커 허브/azure 컨테이너 허브브에 이미지 업로드
# docker login or azr login
# docker tag backend:v1.1 ditlswlwhs3/backend:v1.1
# docker image push ditlswlwhs3/backend:v1.1