#!/bin/sh
python manage.py makemigrations accounts
python manage.py makemigrations clothing
python manage.py makemigrations vtryon
python manage.py migrate  # 데이터베이스 마이그레이션

# 정적파일 자동으로 모으기
python manage.py collectstatic --no-input

# 환경 변수를 사용하여 자동으로 수퍼유저 생성
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

from clothing.models import ClothSubType

User = get_user_model()
if not User.objects.filter(username=os.getenv("DJANGO_SUPERUSER_USERNAME")).exists():
    User.objects.create_superuser(
        os.getenv("DJANGO_SUPERUSER_USERNAME"),
        os.getenv("DJANGO_SUPERUSER_EMAIL"),
        os.getenv("DJANGO_SUPERUSER_PASSWORD")
    )
EOF

# 첫 실행 시 apps.clothing의 ClothSubType 모델에 초기 데이터 추가
# 환경변수 DJANGO_INITIAL_CLOTHSUBTYPE에 쉼표로 구분된 초기 데이터 값이 존재하면 이를 읽어 처리
python manage.py shell <<EOF
import os
from clothing.models import ClothSubType
initial_types_str = os.getenv("DJANGO_INITIAL_CLOTHSUBTYPE", "")

if initial_types_str:
    initial_types = [x.strip() for x in initial_types_str.split(",")]
    for subtype in initial_types:
        if not ClothSubType.objects.filter(name=subtype).exists():
            ClothSubType.objects.create(name=subtype)
EOF

# 배포용 코드
# exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application  # Gunicorn 실행
exec gunicorn --bind 0.0.0.0:8000 --reload config.wsgi:application
