import openai
import base64
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from .models import OCRResult
from .serializers import OCRResultSerializer

<<<<<<< Updated upstream
openai.api_key = "settings.OPENAI_API_KEY"  # OpenAI API 키 설정
=======
openai.api_key = settings.OPENAI_API_KEY  # OpenAI API 키 설정
>>>>>>> Stashed changes

@api_view(['POST'])
@parser_classes([MultiPartParser])
def ocr_image(request):
    if 'image' not in request.FILES:
        return Response({"error": "이미지를 업로드하세요."}, status=400)

    image = request.FILES['image']
    
    # 이미지 파일을 Base64로 변환
    encoded_image = base64.b64encode(image.read()).decode('utf-8')
    
    # OpenAI GPT-4V OCR 요청
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "이 이미지에서 텍스트를 추출해 주세요."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]
        }
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=1000
        )
        ocr_text = response.choices[0].message['content']
        
        # OCR 결과 저장
        ocr_result = OCRResult.objects.create(image=image, text=ocr_text)

        # 네이버 클로바 TTS 변환
        audio_file = generate_tts(ocr_text)
        if audio_file:
            ocr_result.audio.save(f"tts_{ocr_result.id}.mp3", ContentFile(audio_file))

        serializer = OCRResultSerializer(ocr_result)
        return Response(serializer.data)
    
    except Exception as e:
        return Response({"error": str(e)}, status=500)


def generate_tts(text):
    """
    네이버 클로바 TTS API를 사용하여 텍스트를 음성으로 변환하는 함수
    """
    url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
    headers = {
<<<<<<< Updated upstream
        "X-NCP-APIGW-API-KEY-ID": "8419bd554f",
        "X-NCP-APIGW-API-KEY": "p0e0HlCPeyiyCnsVhSICyMQQG4uI31zqW7B4KPO3",
=======
        "X-NCP-APIGW-API-KEY-ID": settings.NAVER_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": settings.NAVER_CLIENT_SECRET,
>>>>>>> Stashed changes
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "speaker": "nara",  # 목소리 유형 (ex: nara, jinho 등)
        "speed": "0",  # 속도 (-5 ~ 5)
        "text": text
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.content  # MP3 파일 데이터 반환
    return None
