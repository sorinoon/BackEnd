import cv2

from ultralytics import solutions, YOLO

model = YOLO("yolo11n.pt")
cap = cv2.VideoCapture("C:/Users/joonh/OneDrive/바탕 화면/Django/YOLO/test.mp4")
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
video_writer = cv2.VideoWriter("speed_estimation.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Initialize SpeedEstimator
speed_obj = solutions.SpeedEstimator(
    region=[(0, 360), (1280, 360)],
    model="yolo11n.pt",
    show=True,
)

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        break
    tracks = model.track(im0,persist=True,show=False)
    print('speed: ',tracks[0].speed)
    im0 = speed_obj.estimate_speed(im0)
    video_writer.write(im0)

cap.release()
video_writer.release()
cv2.destroyAllWindows()

# import cv2
# from ultralytics import YOLO, solutions

# model = YOLO("yolo11n.pt")
# names = model.model.names

# cap = cv2.VideoCapture("C:/Users/joonh/OneDrive/바탕 화면/Django/YOLO/testVideo.mp4")
# w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# video_writer = cv2.VideoWriter("speed_estimation.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# line_pts = [(0,360),(1280,360)]

# speed_obj = solutions.SpeedEstimator(
#      reg_pts = line_pts,
#      names = names,
#      view_img =True,
# )

# while cap.isOpened():
#     success, im0 = cap.read()
#     if not success:
#         break
#     tracks = model.track(im0,persist=True,show =False)
#     print('speed: ',tracks[0].speed)

#     im0 = speed_obj.estimate_speed(im0, tracks)
#     video_writer.write(im0)

