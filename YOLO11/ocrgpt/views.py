import pytesseract
from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import traceback
import openai
#추가
import requests
import uuid
import json

# Tesseract 경로 (Windows인 경우)
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

openai.api_key = "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"
CLOVA_OCR_SECRET = "ZFJSeVJqTEVhcUhPY0l1cVBIT0NsSXJwZWNSdnhQY3E="
CLOVA_OCR_URL = "https://clovapi.ncloud.com/v1/recognizer/text/general"

class OCRSummaryView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': '이미지를 보내주세요'}, status=400)

        # 이미지 → OCR 텍스트 pytessearact
        # image = Image.open(image_file)
        # extracted_text = pytesseract.image_to_string(image, lang='kor+eng')

        # if not extracted_text.strip():
        #     return Response({'error': '텍스트를 추출하지 못했습니다'}, status=400)

        # print(extracted_text)

        image_data = image_file.read()
        headers = {
            "X-OCR-SECRET": CLOVA_OCR_SECRET,
        }
        payload = {
            "images": [
                {
                    "format": "jpg",
                    "name": "sample_image"
                }
            ],
            "requestId": str(uuid.uuid4()),
            "version": "V2",
            "timestamp": int(uuid.uuid1().time // 10000)
        }
        files = {
            'message': (None, json.dumps(payload), 'application/json'),
            'file': (image_file.name, image_data, image_file.content_type)
        }

       
        ocr_response = requests.post(CLOVA_OCR_URL, headers=headers, files=files)
        ocr_result = ocr_response.json()

        #OCR 결과 텍스트 추출
        fields = ocr_result.get('images', [])[0].get('fields', [])
        extracted_text = '\n'.join(field.get('inferText', '') for field in fields)

        if not extracted_text.strip():
            return Response({'error': '텍스트를 추출하지 못했습니다'}, status=400)
            
        print("[OCR 결과]\n", extracted_text)   
    
        # GPT 요약
        prompt = f"다음 글을 짧고 간결하게 요약해줘:\n\n{extracted_text}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            summary = response.choices[0].message.content
            print(summary)
        except Exception as e:
            traceback.print_exc()
            return Response({'error': 'GPT 처리 실패', 'detail': str(e)}, status=500)

        # JSON으로 응답
        return Response({
            "summary": summary.strip()
        })
    
    
