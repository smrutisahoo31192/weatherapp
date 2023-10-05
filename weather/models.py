# weather/models.py

from django.db import models
from django.contrib.auth.models import User


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    search_details = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.location} ({self.timestamp})"
