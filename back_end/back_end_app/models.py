from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name_video = models.CharField(max_length=255)
    title_article = models.CharField(max_length=255)
    video_url = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to='images/')
    keywords = models.CharField(max_length=255, blank=True, null=True)

    def str(self):
        return self.title_article
