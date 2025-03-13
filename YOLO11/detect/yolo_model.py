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
import cv2
import numpy as np
from ultralytics import YOLO

# YOLO 모델 로드
model = YOLO("C:/Users/joonh/OneDrive/바탕 화면/YOLO11/runs/detect/train/weights/best.pt") 

# 카메라 초점 거리 설정
FOCAL_LENGTH = 800
REFERENCE_OBJECT_WIDTH = 50  # 기준 물체의 실제 너비 (cm)
WARNING_DISTANCE = 300  # 3m (300cm)

# 객체별 경고 상태 저장
object_warnings = {}

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        new_warnings = {}

        closest_obj = None  # 가장 가까운 객체 정보
        closest_distance = float('inf')  # 가장 가까운 거리 초기화

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

        # 가장 가까운 객체가 3m 이내일 경우 경고 출력 (한 번만)
        if closest_obj and closest_distance <= WARNING_DISTANCE:
            class_name, distance, obj_id = closest_obj
            if obj_id not in object_warnings or object_warnings[obj_id] > WARNING_DISTANCE:
                print(f"⚠️ 가장 가까운 객체: {class_name} ({distance:.2f} cm)")

        object_warnings.update(new_warnings)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
