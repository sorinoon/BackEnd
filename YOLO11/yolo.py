import torch
from models.common import DetectMultiBackend

# 모델 로드
model = DetectMultiBackend('runs/detect/train/weights/best.pt', device='cpu')  # best.pt 모델 경로

# 더미 입력
dummy_input = torch.randn(1, 3, 640, 640)  # 모델 입력 크기

# 모델을 ONNX 형식으로 내보내기
model.export(format='onnx')  # 'onnx'로 내보내기
