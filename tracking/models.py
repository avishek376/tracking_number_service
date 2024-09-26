from django.db import models

# Create your models here.
# tracking/models.py


class TrackingNumber(models.Model):
    tracking_number = models.CharField(max_length=16, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tracking_number
