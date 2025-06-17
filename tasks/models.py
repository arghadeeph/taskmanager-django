from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    details = models.TextField()
    completed = models.DateTimeField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title