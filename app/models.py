from django.db import models

# USER 모델을 POST에 넣기 위함
from django.conf import settings
# Create your models here.
class Post(models.Model):
    def __str__(self):
        return self.title
    
    title = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    body = models.TextField()
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="writer", default="")
    