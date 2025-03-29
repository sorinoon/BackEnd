# from django.urls import path
# from . import views

# urlpatterns = [
#     path('detect/', views.detect_objects, name='detect_objects'),
# ]

from django.urls import path
from .views import video_feed, api_info

urlpatterns = [
    # path('', index, name='index'),
    path('', api_info, name='api_info'),  # JSON 응답으로 대체
    path('video_feed/', video_feed, name='video_feed'),
]
