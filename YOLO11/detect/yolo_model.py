# import cv2
# import numpy as np
# from ultralytics import YOLO

# # YOLO 모델 로드
# model = YOLO("C:/Users/joonh/OneDrive/바탕 화면/YOLO11/runs/detect/train/weights/best.pt") 

# # 카메라 초점 거리 설정
# FOCAL_LENGTH = 800
# REFERENCE_OBJECT_WIDTH = 50  # 기준 물체의 실제 너비 (cm)
# WARNING_DISTANCE = 300  # 3m (300cm)

# # 객체별 경고 상태 저장
# object_warnings = {}

# def generate_frames(video_path):
#     cap = cv2.VideoCapture(video_path)

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         results = model(frame)
#         new_warnings = {}

#         for result in results:
#             for i, box in enumerate(result.boxes):
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 class_id = int(box.cls[0])
#                 class_name = model.names[class_id]

#                 # 물체의 너비(픽셀)
#                 object_width_pixels = abs(x2 - x1)

#                 # 거리 계산
#                 if object_width_pixels > 0:
#                     distance = (REFERENCE_OBJECT_WIDTH * FOCAL_LENGTH) / object_width_pixels
#                 else:
#                     distance = None  

#                 # 객체 ID 생성
#                 obj_id = f"{class_name}_{(x1 + x2) // 2}_{(y1 + y2) // 2}"
#                 new_warnings[obj_id] = distance

#                 # 3m 이내 접근 시 경고 출력
#                 if distance and distance <= WARNING_DISTANCE:
#                     if obj_id not in object_warnings or object_warnings[obj_id] > WARNING_DISTANCE:
#                         print(f"⚠️ {class_name} 객체가 3m 이내에 있습니다!")

#                 # 감지 결과 표시
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, f"{class_name}: {distance:.2f} cm" if distance else class_name, 
#                             (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

#         object_warnings.update(new_warnings)

#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cap.release()
# import cv2
# import numpy as np
# from ultralytics import YOLO

# # YOLO 모델 로드
# model = YOLO("C:/Users/joonh/OneDrive/바탕 화면/YOLO11/runs/detect/train/weights/best.pt") 

# # 카메라 초점 거리 설정
# FOCAL_LENGTH = 800
# REFERENCE_OBJECT_WIDTH = 50  # 기준 물체의 실제 너비 (cm)
# WARNING_DISTANCE = 300  # 3m (300cm)

# # 객체별 경고 상태 저장
# object_warnings = {}

# def generate_frames(video_path):
#     cap = cv2.VideoCapture(video_path)

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         results = model(frame)
#         new_warnings = {}

#         closest_obj = None  # 가장 가까운 객체 정보
#         closest_distance = float('inf')  # 가장 가까운 거리 초기화

#         for result in results:
#             for box in result.boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 class_id = int(box.cls[0])
#                 class_name = model.names[class_id]

#                 object_width_pixels = abs(x2 - x1)

#                 if object_width_pixels > 0:
#                     distance = (REFERENCE_OBJECT_WIDTH * FOCAL_LENGTH) / object_width_pixels
#                 else:
#                     distance = None  

#                 obj_id = f"{class_name}_{(x1 + x2) // 2}_{(y1 + y2) // 2}"
#                 new_warnings[obj_id] = distance

#                 # 가장 가까운 객체 찾기
#                 if distance and distance < closest_distance:
#                     closest_distance = distance
#                     closest_obj = (class_name, distance, obj_id)

#                 # 감지된 객체 박스 및 거리 표시
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, f"{class_name}: {distance:.2f} cm" if distance else class_name, 
#                             (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

#         # 가장 가까운 객체가 3m 이내일 경우 경고 출력 (한 번만)
#         if closest_obj and closest_distance <= WARNING_DISTANCE:
#             class_name, distance, obj_id = closest_obj
#             if obj_id not in object_warnings or object_warnings[obj_id] > WARNING_DISTANCE:
#                 print(f"⚠️ 가장 가까운 객체: {class_name} ({distance:.2f} cm)")

#         object_warnings.update(new_warnings)

#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cap.release()

# import cv2
# import numpy as np
# from ultralytics import YOLO

# # YOLO 모델 로드
# #model = YOLO("C:/Users/joonh/OneDrive/바탕 화면/YOLO11/runs/detect/train/weights/best.pt") 

# model = YOLO("C:/Users/hansung/Documents/GitHub/BackEnd/YOLO11/runs/detect/train/weights/best.pt")

# # 카메라 초점 거리 설정
# FOCAL_LENGTH = 800
# REFERENCE_OBJECT_WIDTH = 50  # 기준 물체의 실제 너비 (cm)
# WARNING_DISTANCE = 300  # 3m (300cm)

# # 객체별 경고 상태 저장
# object_warnings = {}

# def generate_frames(source=0):  # 🔹 기본값으로 웹캠 사용 (0번 카메라)
#     cap = cv2.VideoCapture(source)
#     #cap.set(cv2.CAP_PROP_FPS, 10)

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         results = model(frame)  # YOLO 모델 적용
#         new_warnings = {}

#         closest_obj = None  
#         closest_distance = float('inf')  

#         for result in results:
#             for box in result.boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 class_id = int(box.cls[0])
#                 class_name = model.names[class_id]

#                 object_width_pixels = abs(x2 - x1)

#                 if object_width_pixels > 0:
#                     distance = (REFERENCE_OBJECT_WIDTH * FOCAL_LENGTH) / object_width_pixels
#                 else:
#                     distance = None  

#                 obj_id = f"{class_name}_{(x1 + x2) // 2}_{(y1 + y2) // 2}"
#                 new_warnings[obj_id] = distance

#                 # 가장 가까운 객체 찾기
#                 if distance and distance < closest_distance:
#                     closest_distance = distance
#                     closest_obj = (class_name, distance, obj_id)

#                 # 감지된 객체 박스 및 거리 표시
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, f"{class_name}: {distance:.2f} cm" if distance else class_name, 
#                             (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

#         # 가장 가까운 객체가 3m 이내일 경우 경고 출력 (한 번만)
#         if closest_obj and closest_distance <= WARNING_DISTANCE:
#             class_name, distance, obj_id = closest_obj
#             if obj_id not in object_warnings or object_warnings[obj_id] > WARNING_DISTANCE:
#                 print(f"⚠️ 가장 가까운 객체: {class_name} ({distance:.2f} cm)")

#         object_warnings.update(new_warnings)

#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cv2.waitKey(10000000000)
#     cap.release()

# import cv2
# import numpy as np
# import requests
# import pygame
# import io
# from ultralytics import YOLO

# # 네이버 클로바 TTS API 설정
# # NAVER_CLIENT_ID = "8419bd554f"  # 네이버 클로바 API 클라이언트 ID
# # NAVER_CLIENT_SECRET = "p0e0HlCPeyiyCnsVhSICyMQQG4uI31zqW7B4KPO3"  # 네이버 클로바 API 클라이언트 Secret
# TTS_URL = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"

# # YOLO 모델 로드
# #model = YOLO("C:/Users/hansung/Documents/GitHub/BackEnd/YOLO11/runs/detect/train/weights/best.pt")

# # 모델 로드
# model = YOLO("runs/detect/train/weights/best.pt")


# # 카메라 초점 거리 설정
# FOCAL_LENGTH = 800
# REFERENCE_OBJECT_WIDTH = 50  # 기준 물체의 실제 너비 (cm)
# WARNING_DISTANCE = 300  # 3m (300cm)

# # 객체별 경고 상태 저장
# object_warnings = {}

# # def play_tts(text):
# #     """네이버 클로바 TTS API를 호출하고 음성을 재생"""
# #     headers = {
# #         "X-NCP-APIGW-API-KEY-ID": "8419bd554f",
# #         "X-NCP-APIGW-API-KEY": "p0e0HlCPeyiyCnsVhSICyMQQG4uI31zqW7B4KPO3",
# #         "Content-Type": "application/x-www-form-urlencoded",
# #     }
# #     data = {
# #         "speaker": "mijin",  # 여성 음성 (다른 옵션: "jinho" - 남성 음성)
# #         "speed": "0",  # 음성 속도 조절 (-5 ~ +5)
# #         "text": text,
# #     }

# #     response = requests.post(TTS_URL, headers=headers, data=data)
# #     if response.status_code == 200:
# #         pygame.mixer.init()
# #         audio_stream = io.BytesIO(response.content)
# #         pygame.mixer.music.load(audio_stream)
# #         pygame.mixer.music.play()
# #         while pygame.mixer.music.get_busy():
# #             continue  # 음성이 끝날 때까지 대기
# #     else:
# #         print("TTS 요청 실패:", response.text)

# def play_tts(text):
#     url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    
#     # 클로바 TTS API의 인증 정보 (클라이언트 ID, 클라이언트 시크릿)
#     client_id = "8419bd554f"
#     client_secret = "1tI9xbELi4xyGC426tPQljd9HPTuPiKELzA3vxx8"
    
#     headers = {
#         'X-Naver-Client-Id': client_id,
#         'X-Naver-Client-Secret': client_secret,
#         'Content-Type': 'application/json'
#     }
    
#     # 요청 데이터 (text가 음성으로 변환될 문장)
#     data = {
#         "speaker": "mijin",   # 사용할 음성 선택 (예: 'clova', 'mijin', 'jinho', 등)
#         "speed": 0,           # 음성 속도
#         "text": text     # 변환할 텍스트
#     }
    
#     response = requests.post(url, headers=headers, json=data)
    
#     if response.status_code == 200:
#         audio_content = response.content
#         # 음성 파일로 저장하거나 바로 재생할 수 있습니다.
#         with open("warning_audio.mp3", "wb") as audio_file:
#             audio_file.write(audio_content)
        
#         # 예시: os.system('mpg321 warning_audio.mp3') 또는 다른 방법으로 음성 파일을 재생할 수 있습니다.
#         # 예: pygame 또는 pydub 등을 사용하여 음성을 직접 재생할 수도 있습니다.
#     else:
#         print(f"Error: {response.status_code}, {response.text}")


# # def generate_frames(source=0):  # 🔹 기본값으로 웹캠 사용 (0번 카메라)
# #     cap = cv2.VideoCapture(source)

# #     while cap.isOpened():
# #         ret, frame = cap.read()
# #         if not ret:
# #             break

# #         results = model(frame)  # YOLO 모델 적용
# #         new_warnings = {}

# #         closest_obj = None  
# #         closest_distance = float('inf')  

# #         for result in results:
# #             for box in result.boxes:
# #                 x1, y1, x2, y2 = map(int, box.xyxy[0])
# #                 class_id = int(box.cls[0])
# #                 class_name = model.names[class_id]

# #                 object_width_pixels = abs(x2 - x1)

# #                 if object_width_pixels > 0:
# #                     distance = (REFERENCE_OBJECT_WIDTH * FOCAL_LENGTH) / object_width_pixels
# #                 else:
# #                     distance = None  

# #                 obj_id = f"{class_name}_{(x1 + x2) // 2}_{(y1 + y2) // 2}"
# #                 new_warnings[obj_id] = distance

# #                 # 가장 가까운 객체 찾기
# #                 if distance and distance < closest_distance:
# #                     closest_distance = distance
# #                     closest_obj = (class_name, distance, obj_id)

# #                 # 감지된 객체 박스 및 거리 표시
# #                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
# #                 cv2.putText(frame, f"{class_name}: {distance:.2f} cm" if distance else class_name, 
# #                             (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# #         # 가장 가까운 객체가 3m 이내일 경우 경고음 출력 (한 번만)
# #         if closest_obj and closest_distance <= WARNING_DISTANCE:
# #             class_name, distance, obj_id = closest_obj
# #             if obj_id not in object_warnings or object_warnings[obj_id] > WARNING_DISTANCE:
# #                 warning_text = f"경고! {class_name}이 {distance:.0f}cm 앞에 있습니다."
# #                 print(f"⚠️ {warning_text}")
# #                 play_tts(warning_text)  # 🔹 네이버 TTS 호출하여 경고음 출력

# #         object_warnings.update(new_warnings)

# #         _, buffer = cv2.imencode('.jpg', frame)
# #         frame_bytes = buffer.tobytes()

# #         yield (b'--frame\r\n'
# #                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# #     cv2.waitKey(10000000000)
# #     cap.release()

# def generate_frames(source=0):  # 🔹 기본값으로 웹캠 사용 (0번 카메라)
#     cap = cv2.VideoCapture(source)

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         results = model(frame)  # YOLO 모델 적용
#         new_warnings = {}

#         closest_obj = None  
#         closest_distance = float('inf')  

#         for result in results:
#             for box in result.boxes:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 class_id = int(box.cls[0])
#                 class_name = model.names[class_id]

#                 object_width_pixels = abs(x2 - x1)

#                 if object_width_pixels > 0:
#                     distance = (REFERENCE_OBJECT_WIDTH * FOCAL_LENGTH) / object_width_pixels
#                 else:
#                     distance = None  

#                 obj_id = f"{class_name}_{(x1 + x2) // 2}_{(y1 + y2) // 2}"
#                 new_warnings[obj_id] = distance

#                 # 가장 가까운 객체 찾기
#                 if distance and distance < closest_distance:
#                     closest_distance = distance
#                     closest_obj = (class_name, distance, obj_id)

#                 # 감지된 객체 박스 및 거리 표시
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 cv2.putText(frame, f"{class_name}: {distance:.2f} cm" if distance else class_name, 
#                             (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

#         # 가장 가까운 객체가 3m 이내일 경우 경고음 출력 (한 번만)
#         if closest_obj and closest_distance <= WARNING_DISTANCE:
#             class_name, distance, obj_id = closest_obj
#             if obj_id not in object_warnings or object_warnings[obj_id] > WARNING_DISTANCE:
#                 warning_text = f"경고! {class_name}이 {distance:.0f}cm 앞에 있습니다."
#                 print(f"⚠️ {warning_text}")
#                 play_tts(warning_text)  # 🔹 네이버 TTS 호출하여 경고음 출력

#         object_warnings.update(new_warnings)

#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     cv2.waitKey(10000000000)
#     cap.release()

import cv2
import numpy as np
import requests
import pygame
import io
from ultralytics import YOLO
import urllib.request

# 네이버 클로바 TTS API 설정
TTS_URL = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"

# YOLO 모델 로드
model = YOLO("runs/detect/train/weights/best.pt")

# 카메라 초점 거리 설정
FOCAL_LENGTH = 800
REFERENCE_OBJECT_WIDTH = 50  # 기준 물체의 실제 너비 (cm)
WARNING_DISTANCE = 300  # 3m (300cm)

# 객체별 경고 상태 저장
object_warnings = {}

import pygame
import io
import urllib.request

def play_tts(text):
    # 클로바 TTS API의 인증 정보 (클라이언트 ID, 클라이언트 시크릿)
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


def generate_frames(source=0):  # 🔹 기본값으로 웹캠 사용 (0번 카메라)
    cap = cv2.VideoCapture(source)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)  # YOLO 모델 적용
        new_warnings = {}

        closest_obj = None  
        closest_distance = float('inf')  

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                object_width_pixels = abs(x2 - x1)

                if object_width_pixels > 0:
                    distance = (REFERENCE_OBJECT_WIDTH * FOCAL_LENGTH) / object_width_pixels
                else:
                    distance = None  

                obj_id = f"{class_name}_{(x1 + x2) // 2}_{(y1 + y2) // 2}"
                new_warnings[obj_id] = distance

                # 가장 가까운 객체 찾기
                if distance and distance < closest_distance:
                    closest_distance = distance
                    closest_obj = (class_name, distance, obj_id)

                # 감지된 객체 박스 및 거리 표시
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name}: {distance:.2f} cm" if distance else class_name, 
                            (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # 가장 가까운 객체가 3m 이내일 경우 경고음 출력 (한 번만)
        if closest_obj and closest_distance <= WARNING_DISTANCE:
            class_name, distance, obj_id = closest_obj
            if obj_id not in object_warnings or object_warnings[obj_id] > WARNING_DISTANCE:
                warning_text = f"경고! {class_name}이 {distance:.0f}cm 앞에 있습니다."
                print(f"⚠️ {warning_text}")
                play_tts(warning_text)  # 🔹 네이버 TTS 호출하여 경고음 출력

        object_warnings.update(new_warnings)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    cap.release()
