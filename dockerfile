# Alpine Linux 3.13에서 Python 3.7 기반
FROM python:3.7-alpine3.13
WORKDIR /usr/src/app

# 이미지 정보
LABEL maintainer="jonghyeon"

# Pillow 등 의존성 설치를 위한 패키지 추가
RUN apk add --no-cache zlib-dev jpeg-dev gcc musl-dev dos2unix

# Python 패키지 설치
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# entrypoint.sh 파일 복사 및 줄바꿈 변환 및 실행 권한 부여
COPY entrypoint.sh /entrypoint.sh
RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh

# 포트 8000 노출
EXPOSE 8000

# 실행 명령어
ENTRYPOINT ["sh", "/entrypoint.sh"]



# 기본적으로 컨테이너 생성시 루트 계정을 사용한다
# 보안적으로 좋지 않으므로 일반계정을 생성 후 사용용
# RUN useradd -m django-user
# USER django-user

# 도커 이미지 생성
# docker build -t backend:v1.2 .


# 도커 실행 ( --restart always)
# docker run --env-file .env/docker.env --env-file .env/ai_info.env --env-file .env/init_data.env --env-file .env/django.env -itd -p 8000:8000 -v "C:\Users\009\Desktop\WheelWear\WheelWear-Backend-v1":/usr/src/app/ --name backend_v1.3 --link aiserver:aiserver backend:v1.3

# 클라우드 서비스에서 도커 실행
# docker run --env-file .env/docker.env --env-file .env/ai_info.env --env-file .env/init_data.env --env-file .env/django.env -itd -p 8000:8000 --name backend_v1.3 backend:v1.3

# 도커 허브/azure 컨테이너 허브브에 이미지 업로드
# docker login or azr login
# docker tag backend:v1.3 ditlswlwhs3/backend:v1.3
# docker image push ditlswlwhs3/backend:v1.3