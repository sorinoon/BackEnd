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
import cv2
import numpy as np
import requests
import pygame
import io
import urllib.request

openai.api_key = "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"  # OpenAI API 키 설정

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
    client_id = "8419bd554f"
    client_secret = "1tI9xbELi4xyGC426tPQljd9HPTuPiKELzA3vxx8"
    
    encText = text
    data = "speaker=nara&volume=0&speed=0&pitch=0&format=mp3&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)
    
    try:
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()  # getcode()로 응답 코드 확인
        
        if rescode == 200:
            print("TTS mp3 저장")
            response_body = response.read()
            
            # 이후 pygame을 이용해 mp3를 재생
            pygame.mixer.init()
            audio_stream = io.BytesIO(response_body)
            pygame.mixer.music.load(audio_stream)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                continue  # 음성이 끝날 때까지 대기
        else:
            print(f"Error Code: {rescode}")
    
    except Exception as e:
        print(f"Error: {e}")
