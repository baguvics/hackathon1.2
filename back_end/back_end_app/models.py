from django.db import models

class Expmm:
    pass


class Article(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE) Потом добавим, когда глянем, весь ли функционал в дефолтном User подойдет
    video_url = models.CharField(max_length=255)
    content = models.TextField()

