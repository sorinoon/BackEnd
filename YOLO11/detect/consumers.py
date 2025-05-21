import json
import cv2
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from PIL import Image
import io
import torch
from asgiref.sync import async_to_sync
import base64
from ultralytics import YOLO

class YoloDetectConsumer(AsyncWebsocketConsumer):
    model = None

    async def connect(self):
        # 모델 로딩 (처음 연결 시에만)
        if YoloDetectConsumer.model is None:
            YoloDetectConsumer.model = YOLO("runs/detect/train/weights/best.pt")

        # WebSocket 연결 수립
        self.room_name = "yolo_room"
        self.room_group_name = f"yolo_{self.room_name}"

        # 방에 가입
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # 클라이언트에 WebSocket 연결 수락 메시지 보내기
        await self.accept()

    async def disconnect(self, close_code):
        # WebSocket 연결 종료 시 방에서 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("[WebSocket] 메시지 수신됨")
        # 클라이언트로부터 메시지 받음 (이미지 데이터 포함)
        data = json.loads(text_data)
        image_data = data.get('image')  # base64 인코딩된 이미지 데이터

        print(f"[WebSocket] 이미지 데이터 길이: {len(image_data)}")
        # 이미지를 디코딩하고 YOLO 모델 실행
        result = await self.process_yolo_and_tts(image_data)

        # 처리 결과를 WebSocket을 통해 클라이언트로 전달
        await self.send(text_data=json.dumps(result))

    # async def process_yolo_and_tts(self, image_data):
    #     try:
    #         # 이미지 데이터 디코딩
    #         img_bytes = base64.b64decode(image_data)
    #         image = Image.open(io.BytesIO(img_bytes))
    #         frame = np.array(image)
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #         # YOLO 모델 실행
    #         results = YoloDetectConsumer.model(frame)

    #         detected_objects = []
    #         closest_obj = None
    #         closest_distance = float('inf')

    #         for box in results.xywh[0]:  # YOLO 모델 결과
    #             x1, y1, x2, y2 = map(int, box[:4])
    #             class_id = int(box[5])  # 클래스 ID
    #             class_name = YoloDetectConsumer.model.names[class_id]
    #             object_width_pixels = abs(x2 - x1)

    #             # 거리 계산 (간단한 예시)
    #             if object_width_pixels > 0:
    #                 distance = (30 * 615) / object_width_pixels  # 예시
    #             else:
    #                 distance = None

    #             detected_objects.append({
    #                 "class": class_name,
    #                 "distance_cm": round(distance, 2) if distance else None,
    #                 "bounding_box": [x1, y1, x2, y2]
    #             })

    #             if distance and distance < closest_distance:
    #                 closest_distance = distance
    #                 closest_obj = class_name

    #         # 경고 메시지
    #         warning = None
    #         if closest_obj and closest_distance <= 300:  # 3미터 이내
    #             warning = f"{closest_obj}이 {int(closest_distance)}센티미터 앞에 있습니다."

    #         return {
    #             "message": "YOLO 감지 결과",
    #             "detected_objects": detected_objects,
    #             "warning": warning
    #         }

    #     except Exception as e:
    #         print(f"YOLO 처리 중 오류: {e}")
    #         return {"error": str(e)}
    async def process_yolo_and_tts(self, image_data):
        try:
            # 이미지 디코딩
            img_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            frame = np.array(image)

            # YOLOv8 모델 실행
            results = YoloDetectConsumer.model(frame)[0]  # 첫 결과만 사용
            boxes = results.boxes

            detected_objects = []
            closest_obj = None
            closest_distance = float('inf')

            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                class_id = int(box.cls[0])
                class_name = YoloDetectConsumer.model.names[class_id]
                object_width_pixels = abs(x2 - x1)

                # 거리 계산
                distance = (30 * 615) / object_width_pixels if object_width_pixels > 0 else None

                detected_objects.append({
                    "class": class_name,
                    "distance_cm": round(distance, 2) if distance else None,
                    "bounding_box": [x1, y1, x2, y2]
                })

                if distance and distance < closest_distance:
                    closest_distance = distance
                    closest_obj = class_name

            # 안내 메시지 구성
            warning = None
            if closest_obj and closest_distance <= 300:
                warning = f"{closest_obj}이 {int(closest_distance)}센티미터 앞에 있습니다."

            return {
                "message": "YOLO 감지 결과",
                "detected_objects": detected_objects,
                "warning": warning
            }

        except Exception as e:
            print(f"YOLO 처리 중 오류: {e}")
            return {"error": str(e)}
