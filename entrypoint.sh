#!/bin/sh
python manage.py makemigrations
python manage.py migrate  # 데이터베이스 마이그레이션

# 정적파일 자동으로 모으기
python manage.py collectstatic --noinput

# 환경 변수를 사용하여 자동으로 수퍼유저 생성
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username=os.getenv("DJANGO_SUPERUSER_USERNAME")).exists():
    User.objects.create_superuser(
        os.getenv("DJANGO_SUPERUSER_USERNAME"),
        os.getenv("DJANGO_SUPERUSER_EMAIL"),
        os.getenv("DJANGO_SUPERUSER_PASSWORD")
    )
EOF

# 배포용 코드
# exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application  # Gunicorn 실행
exec gunicorn --bind 0.0.0.0:8000 --reload config.wsgi:application
