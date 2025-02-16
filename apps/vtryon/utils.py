import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse
import os

def download_and_save_image(instance, image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image_name = os.path.basename(urlparse(image_url).path)  # URL에서 파일명 추출
        instance.image.save(image_name, ContentFile(response.content), save=True)
