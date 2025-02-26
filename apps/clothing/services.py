import environ
import requests
import json

env = environ.Env()

def map_cloth_type(cloth_type: str) -> str:
    """
    영어 의류 타입을 한글로 매핑합니다.
    매핑이 없으면 원본 값을 그대로 반환합니다.
    """
    mapping = {
        "Top": "상의",
        "Bottom": "바지",
        "Dress": "원피스"
    }
    return mapping.get(cloth_type, cloth_type)
def map_gender(gender: str) -> str:
    """
    영어 성별을 한글로 매핑합니다.
    매핑이 없으면 원본 값을 그대로 반환합니다.
    """
    mapping = {
        "M": "남성",
        "F": "여성"
    }
    return mapping.get(gender, gender)

def get_ai_result(
    brand: str, 
    cloth_size: str, 
    cloth_type: str, 
    gender: str, 
    chest_circumference: float, 
    shoulder_width: float, 
    arm_length: float, 
    waist_circumference: float,
    request
) -> dict:
    """
    환경변수에 설정된 AI 서버 정보를 이용해 외부 AI 서버와 통신하여 
    의류 사이즈 추천을 해줍니다.
    
    Parameters:
        brand (str): 의류 브랜드.
        cloth_size (str): 의류 사이즈.
        cloth_type (str): 의류 타입 (예: "Top", "Bottom", "Dress").
        gender (str): 성별.
        chest_circumference (float): 가슴 둘레.
        shoulder_width (float): 어깨 너비.
        arm_length (float): 팔 길이.
        waist_circumference (float): 허리 둘레.
    
    Returns:
        dict: AI 서버에서 반환한 결과 (JSON 형식 파싱).
    
    Raises:
        Exception: AI 서버와의 통신 중 오류 발생 시.
    """
    # 의류 타입 한글 매핑
    mapped_cloth_type = map_cloth_type(cloth_type)

    # AI 서버 기본 URL 구성
    protocol = env("AI_SERVER_PROTOCOL")
    host = env("AI_SERVER_HOST")
    base_url = f"{protocol}://{host}"
    
    # 타임아웃 값 (기본 300초)
    timeout = env.int("AI_SERVER_TIMEOUT", default=300)
    
    # API 엔드포인트 URL
    ai_url = f"{base_url}/recommend_size"
    
    # AI 서버에 전송할 데이터
    data = {
        "brand": brand,
        "cloth_size": cloth_size,
        "cloth_type": mapped_cloth_type,
        "gender": map_gender(gender),
        "chest_circumference": chest_circumference,
        "shoulder_width": shoulder_width,
        "arm_length": arm_length,
        "waist_circumference": waist_circumference,
    }
    
    print("Sending data to AI server:", json.dumps(data))
    
    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true",
    }
    
    try:
        response = requests.post(ai_url, json=data, headers=headers, timeout=timeout)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
        result = response.json()
        print("Received response from AI server:", result)
        return result
    except requests.RequestException as e:
        error_message = f"AI 서버와 통신 중 문제가 발생했습니다: {str(e)}"
        print(error_message)
        raise Exception(error_message)
