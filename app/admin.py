from django.contrib import admin
from .models import Post, Comment, Hashtag, Relationship

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Hashtag)
admin.site.register(Relationship)