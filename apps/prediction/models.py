from django.conf import settings
from django.db import models


class PredictionLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='predictions',
    )
    input_features = models.JSONField()
    predicted_class = models.CharField(max_length=16)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
