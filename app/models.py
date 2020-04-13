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
    
    image = models.ImageField(upload_to='images/', blank=True)
    
    hashtag = models.CharField(max_length=200, blank=True)
    hashtags = models.ManyToManyField('Hashtag', blank=True)

class Comment(models.Model):
    def __str__(self):
        return self.text
    
    c_writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="c_writer", default="")
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name ="comments")
    text = models.CharField(max_length=100)

class Hashtag(models.Model):
    def __str__(self):
        return self.name
    
    name = models.CharField(max_length=50)

class Relationship(models.Model):
    who = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="who", on_delete=models.CASCADE)
    whom = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="whom", on_delete=models.CASCADE)

    