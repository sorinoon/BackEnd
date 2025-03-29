# import torch
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from PIL import Image
# from io import BytesIO
# from ultralytics import YOLO

# # 모델 로드 (한 번만 로드되도록 하기)
# model = YOLO("C:\Users\joonh\OneDrive\바탕 화면\YOLO11\runs\detect\train\weights\best.pt")  # 학습된 YOLO 모델

# @csrf_exempt  # CSRF 토큰을 제외한 요청을 허용
# def detect_objects(request):
#     if request.method == "POST":
#         # 요청에서 이미지를 가져오기
#         image_file = request.FILES.get("image")  # 이미지 파일 가져오기

#         if image_file:
#             # 이미지를 PIL 이미지로 변환
#             image = Image.open(image_file)

#             # 이미지를 모델에 입력하고 예측 수행
#             results = model(image)  # 이미지를 모델에 전달하여 결과 얻기

#             # 예측된 객체들의 정보를 얻기
#             predictions = results.pandas().xywh[0].to_dict(orient="records")  # 예측 결과를 딕셔너리로 변환

#             return JsonResponse({"predictions": predictions}, status=200)
#         else:
#             return JsonResponse({"error": "No image provided"}, status=400)
#     else:
#         return JsonResponse({"error": "Invalid method"}, status=405)

# import torch
# import cv2
# import numpy as np
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from PIL import Image
# from io import BytesIO
# from ultralytics import YOLO

# # 모델 로드 (한 번만 로드되도록 하기)
# model = YOLO("C:\Users\joonh\OneDrive\바탕 화면\YOLO11\runs\detect\train\weights\best.pt")  # 학습된 YOLO 모델

# # 카메라의 초점 거리와 실제 물체의 높이를 설정
# FOCAL_LENGTH = 800  # 예시로 설정한 초점 거리 (픽셀 단위)
# REAL_OBJECT_HEIGHT = 1.7  # 예시로 설정한 실제 물체의 높이 (미터, 사람 평균 높이)

# @csrf_exempt
# def detect_objects(request):
#     if request.method == "POST":
#         # 요청에서 이미지를 가져오기
#         image_file = request.FILES.get("image")  # 이미지 파일 가져오기

#         if image_file:
#             # 이미지를 PIL 이미지로 변환
#             image = Image.open(image_file)

#             # 이미지를 모델에 입력하고 예측 수행
#             results = model(image)

#             # 예측된 객체들의 정보를 얻기
#             predictions = results.pandas().xywh[0].to_dict(orient="records")

#             # 거리 계산
#             for prediction in predictions:
#                 object_height_in_image = prediction['height']
#                 if object_height_in_image > 0:
#                     distance = (FOCAL_LENGTH * REAL_OBJECT_HEIGHT) / object_height_in_image
#                     prediction["distance"] = distance  # 예측 결과에 거리 정보 추가
#                 else:
#                     prediction["distance"] = "N/A"  # 높이가 0일 경우 거리 계산 불가

#             return JsonResponse({"predictions": predictions}, status=200)
#         else:
#             return JsonResponse({"error": "No image provided"}, status=400)
#     else:
#         return JsonResponse({"error": "Invalid method"}, status=405)
# from django.http import StreamingHttpResponse
# from django.shortcuts import render
# from .yolo_model import generate_frames

# VIDEO_PATH = "C:/Users/joonh/OneDrive/바탕 화면/Django/YOLO/testVideo.mp4"

# def video_feed(request):
#     return StreamingHttpResponse(generate_frames(VIDEO_PATH), content_type="multipart/x-mixed-replace; boundary=frame")

# def index(request):
#     return render(request, 'index.html')

from django.shortcuts import render
from .yolo_model import generate_frames
from django.http import StreamingHttpResponse, JsonResponse

def video_feed(request):
    return StreamingHttpResponse(generate_frames(0), content_type="multipart/x-mixed-replace; boundary=frame")

def api_info(request):
    return JsonResponse({"message": "Django API is working!"})  # JSON 응답 추가