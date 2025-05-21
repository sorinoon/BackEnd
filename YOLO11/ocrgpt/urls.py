# ocrapp/urls.py
from django.urls import path
from .views import OCRSummaryView

urlpatterns = [
    path('ocr-summary/', OCRSummaryView.as_view()),
]
