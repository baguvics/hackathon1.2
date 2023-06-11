from django.db import models
from django.contrib.auth.models import AbstractUser, User



class Article(models.Model):
    video_url = models.CharField(max_length=255)
    content = models.TextField()


# модель для хранения информации о подтверждении email
class EmailConfirmation(models.Model):                          
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    confirmed = models.BooleanField(default=False)