from ultralytics import YOLO

model = YOLO("yolo11n.pt")

train_results = model.train(
    data="coco8.yaml",  # Path to dataset configuration file
    epochs=100,  # Number of training epochs
    imgsz=640,  # Image size for training
    device="cuda",  # Device to run on (e.g., 'cpu', 0, [0,1,2,3])
)

metrics = model.val()

results = model
results[0].show()

path = model.export(format="onnx")