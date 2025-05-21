from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from ultralytics import YOLO
import cv2
import numpy as np
import urllib.request
import urllib.parse
import io
from django.http import FileResponse
from .task import process_yolo_and_tts
FOCAL_LENGTH = 615
REFERENCE_OBJECT_WIDTH = 30  # cm
WARNING_DISTANCE = 300  # 3미터

class YoloDetectView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({"error": "No image provided"}, status=400)
        process_yolo_and_tts.delay(image_file)  # Celery 백그라운드 작업 호출
        return Response({"message": "Processing started"}, status=202)
    
        # file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        # frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # model_path = "runs/detect/train/weights/best.pt"
        # try:
        #     model = YOLO(model_path)
        #     results = model(frame)
        # except Exception as e:
        #     print(f"YOLO 처리 중 오류: {e}")
        #     return Response({"error": "YOLO 처리 실패", "detail": str(e)}, status=500)

        # result = results[0]
        # detected_objects = []
        # closest_obj = None
        # closest_distance = float('inf')

        # for box in result.boxes:
        #     x1, y1, x2, y2 = map(int, box.xyxy[0])
        #     class_id = int(box.cls[0])
        #     class_name = model.names[class_id]
        #     object_width_pixels = abs(x2 - x1)

        #     if object_width_pixels > 0:
        #         distance = (REFERENCE_OBJECT_WIDTH * FOCAL_LENGTH) / object_width_pixels
        #     else:
        #         distance = None

        #     detected_objects.append({
        #         "class": class_name,
        #         "distance_cm": round(distance, 2) if distance else None,
        #         "bounding_box": [x1, y1, x2, y2]
        #     })

        #     if distance and distance < closest_distance:
        #         closest_distance = distance
        #         closest_obj = class_name

        # if closest_obj and closest_distance <= WARNING_DISTANCE:
        #     warning_text = f"{closest_obj}이 {int(closest_distance)}센티미터 앞에 있습니다."
        #     print(f"⚠️ {warning_text}")

        #     tts_audio = self.get_tts_audio(warning_text)
        #     if tts_audio:
        #         return FileResponse(
        #             tts_audio,
        #             content_type='audio/mpeg',
        #             as_attachment=False,
        #             filename="warning.mp3"
        #         )
        #     else:
        #         return Response({"error": "TTS generation failed"}, status=500)

        # return Response({"detected": detected_objects})

    def get_tts_audio(self, text):
        client_id = "8419bd554f"
        client_secret = "1tI9xbELi4xyGC426tPQljd9HPTuPiKELzA3vxx8"

        data = "speaker=nara&volume=0&speed=0&pitch=0&format=mp3&text=" + urllib.parse.quote(text)
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)

        try:
            response = urllib.request.urlopen(request, data=data.encode('utf-8'))
            if response.getcode() == 200:
                return io.BytesIO(response.read())
            else:
                print(f"TTS Error Code: {response.getcode()}")
                return None
        except Exception as e:
            print(f"TTS Exception: {e}")
            return None
# from rest_framework.views import APIView
# from rest_framework.parsers import MultiPartParser
# from rest_framework.response import Response
# from rest_framework import status
# from .task import process_yolo_and_tts  # Celery 작업 호출

# class YoloDetectView(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request):
#         image_file = request.FILES.get('image')
#         if not image_file:
#             return Response({"error": "No image provided"}, status=400)

#         # Celery 백그라운드 작업 호출 (이미지 파일을 처리할 작업 큐에 넣음)
#         process_yolo_and_tts.delay(image_file.read())

#         # 클라이언트에게 "Processing started" 응답을 즉시 반환
#         return Response({"message": "Processing started"}, status=202)
