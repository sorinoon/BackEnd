from django.urls import path
from .views import YoloDetectView

urlpatterns = [
    path('detect/', YoloDetectView.as_view(), name='yolo-detect'),
]
