from ultralytics import YOLO

# Load a model
if __name__ == "__main__":
    # 첫 번째 방법: YAML 파일로부터 모델을 빌드하고 가중치를 불러옵니다.
    model = YOLO("yolo11n.yaml")  # 모델 빌드
    model.load("yolo11n.pt")  # 가중치 불러오기
    
    # 또는 두 번째 방법: YAML 파일로부터 모델을 빌드하고 훈련을 위한 프리트레인된 모델을 불러옵니다.
    # model = YOLO("yolo11n.pt")  # 프리트레인된 모델 바로 불러오기
    
    # Train the model
    results = model.train(data="coco8.yaml", epochs=100, imgsz=640)
