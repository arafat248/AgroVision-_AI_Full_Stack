import uuid
from django.db import models
from django.conf import settings

class PredictionHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictions')
    predicted_crop = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    risk_level = models.CharField(max_length=50)
    
    # Inputs parameters
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Prediction History'
        verbose_name_plural = 'Prediction Histories'
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.user.email} - {self.predicted_crop} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"