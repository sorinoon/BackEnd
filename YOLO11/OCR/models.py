from django.db import models

# Create your models here.

class OCRResult(models.Model):
    image = models.ImageField(upload_to='ocr_images/')
    text = models.TextField()
    audio = models.FileField(upload_to='tts_audio/', null=True, blank=True)  # TTS 음성 파일 추가
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OCRResult {self.id} - {self.created_at}"
