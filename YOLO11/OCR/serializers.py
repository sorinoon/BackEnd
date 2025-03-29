from rest_framework import serializers
from .models import OCRResult

class OCRResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRResult
        fields = '__all__'
