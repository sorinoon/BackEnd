import pytesseract
from PIL import Image
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import traceback
import openai

# Tesseract 경로 (Windows인 경우)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

openai.api_key = "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"

class OCRSummaryView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': '이미지를 보내주세요'}, status=400)

        # 이미지 → OCR 텍스트
        image = Image.open(image_file)
        extracted_text = pytesseract.image_to_string(image, lang='kor')

        if not extracted_text.strip():
            return Response({'error': '텍스트를 추출하지 못했습니다'}, status=400)

        print(extracted_text)
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
