from django.urls import path
from .views import ocr_image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('ocr/', ocr_image, name='ocr_image'),
]

# 미디어 파일 접근 가능하도록 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
