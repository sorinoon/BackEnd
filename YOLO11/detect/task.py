# from celery import shared_task
# from ultralytics import YOLO
# import numpy as np
# import cv2

# @shared_task
# def process_yolo_and_tts(image_file):
#     # YOLO 모델과 TTS 처리 로직
#     model = YOLO("runs/detect/train/weights/best.pt")
#     file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
#     frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = model(frame)
#     # TTS 생성을 비동기적으로 처리하는 로직
#     return results

from celery import shared_task
from ultralytics import YOLO
import numpy as np
import cv2
import io
import urllib.request
import urllib.parse
from django.http import FileResponse

FOCAL_LENGTH = 615
REFERENCE_OBJECT_WIDTH = 30  # cm
WARNING_DISTANCE = 300  # 3미터

@shared_task
def process_yolo_and_tts(image_data):
    try:
        # 이미지 처리
        file_bytes = np.asarray(bytearray(image_data), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # YOLO 모델 로드
        model_path = "runs/detect/train/weights/best.pt"
        model = YOLO(model_path)
        results = model(frame)

        # 객체 탐지
        result = results[0]
        detected_objects = []
        closest_obj = None
        closest_distance = float('inf')

        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            object_width_pixels = abs(x2 - x1)

            if object_width_pixels > 0:
                distance = (REFERENCE_OBJECT_WIDTH * FOCAL_LENGTH) / object_width_pixels
            else:
                distance = None

            detected_objects.append({
                "class": class_name,
                "distance_cm": round(distance, 2) if distance else None,
                "bounding_box": [x1, y1, x2, y2]
            })

            if distance and distance < closest_distance:
                closest_distance = distance
                closest_obj = class_name

        # 경고: 물체가 너무 가까운 경우
        if closest_obj and closest_distance <= WARNING_DISTANCE:
            warning_text = f"{closest_obj}이 {int(closest_distance)}센티미터 앞에 있습니다."
            print(f"⚠️ {warning_text}")

            # TTS 생성
            tts_audio = get_tts_audio(warning_text)
            if tts_audio:
                # 필요에 따라 결과를 저장하거나 다른 방법으로 처리할 수 있습니다
                return FileResponse(tts_audio, content_type='audio/mpeg', as_attachment=False, filename="warning.mp3")

        return detected_objects  # 객체 감지 결과만 반환

    except Exception as e:
        print(f"Error during processing: {e}")
        return None

def get_tts_audio(text):
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
            return io.BytesIO(response.read())  # TTS 음성 데이터를 메모리로 반환
        else:
            print(f"TTS Error Code: {response.getcode()}")
            return None
    except Exception as e:
        print(f"TTS Exception: {e}")
        return None
