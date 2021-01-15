from datetime import datetime
from django.db import models
import uuid


class SecretMessage(models.Model):
    Id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    MessageContent = models.CharField(max_length=512)
    ExpirationSec = models.IntegerField(default=20)
    CreationTime = models.DateTimeField(default=datetime.now)
    ReadingTime = models.DateTimeField(default=datetime.now)
    IsRead = models.BooleanField(default=False)


