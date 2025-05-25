from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/yolo/', include('detect.urls')),
    #path('',include('OCR.urls'))
    path('', include('ocrgpt.urls')),
]


