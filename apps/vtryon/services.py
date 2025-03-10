import environ
import requests
import json

env = environ.Env()
def map_cloth_type(cloth_type):
    mapping = {
        "Top": "upper",
        "Bottom": "lower",
        "Dress": "overall"
    }
    return mapping.get(cloth_type, cloth_type)

def get_absolute_url(url, request):
    """ 상대 URL인 경우 절대 URL로 변환 """
    if url and not url.startswith("http"):
        return request.build_absolute_uri(url)
    return url

def get_ai_result_image(top_cloth, bottom_cloth, dress_cloth, body_image, vton_image, cloth_type, request):
    """
    환경변수에 설정된 AI 서버 정보를 이용해 외부 AI 서버와 통신
    """
    cloth_type = map_cloth_type(cloth_type)

    base_url = env("AI_SERVER_PROTOCOL")+'://'+env("AI_SERVER_HOST")

    timeout = env.int("AI_SERVER_TIMEOUT", default=120)
    
    # API 엔드포인트 구성 (예: /api/tryon)
    ai_url = f"{base_url}/tryon"
    
    payload = {
        "cloth_type": cloth_type
    }
    if vton_image:
        payload["body_image_url"] = vton_image.image
    else:
        payload["body_image_url"] = get_absolute_url(body_image.body_image.url, request)
        
        
    if cloth_type == "upper":
        payload["top_cloth_url"] = get_absolute_url(top_cloth.clothImage.url, request)
    elif cloth_type == "lower":
        payload["bottom_cloth_url"] = get_absolute_url(bottom_cloth.clothImage.url, request)
    elif cloth_type == "overall":
        payload["dress_image_url"] = get_absolute_url(dress_cloth.clothImage.url, request)

    print(json.dumps(payload))
    
    try:
        headers = {
            "Content-Type": "application/json",
            "ngrok-skip-browser-warning" : "true",
        }
        response = requests.post(ai_url, json=payload, headers=headers, timeout=timeout)
        response.raise_for_status() # 응답 오류 시 예외 발생
        result = response.json()
        print(result)
        return result.get("result_image_url")
    except requests.RequestException as e:
        raise Exception(f"AI 서버와 통신 중 문제가 발생했습니다: {str(e)}")
