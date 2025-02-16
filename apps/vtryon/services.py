import environ
import requests

env = environ.Env()

def get_ai_result_image(top_cloth, bottom_cloth, dress_cloth, body_image):
    """
    환경변수에 설정된 AI 서버 정보를 이용해 외부 AI 서버와 통신
    """

    base_url = env("AI_SERVER_PROTOCOL")+'://'+env("AI_SERVER_HOST")

    timeout = env.int("AI_SERVER_TIMEOUT", default=120)
    
    # API 엔드포인트 구성 (예: /api/tryon)
    ai_url = f"{base_url}/tryon"
    
    payload = {
        "top_cloth_url": top_cloth.clothImage.url if top_cloth and top_cloth.clothImage else None,
        "bottom_cloth_url": bottom_cloth.clothImage.url if bottom_cloth and bottom_cloth.clothImage else None,
        "body_image_url": body_image.body_image.url if body_image and body_image.body_image else None,
        "dress_image_url": dress_cloth.clothImage.url if dress_cloth and dress_cloth.clothImage else None,
    }
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(ai_url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status() # 응답 오류 시 예외 발생
        result = response.json()
        
        return base_url+result.get("result_image_url")
    except requests.RequestException as e:
        raise Exception(f"AI 서버와 통신 중 문제가 발생했습니다: {str(e)}")
