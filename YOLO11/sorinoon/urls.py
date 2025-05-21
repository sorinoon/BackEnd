from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/yolo/', include('detect.urls')),  # your_app의 URL 
    #path('',include('OCR.urls'))
    path('', include('ocrgpt.urls')),
]


