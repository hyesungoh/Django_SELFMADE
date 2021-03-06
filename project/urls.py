"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# for img uploader
from django.conf import settings
from django.conf.urls.static import static

import app.views 
import count.views
from diary.views import diary_home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.home, name="home"),
    path('write', app.views.write, name="write"),
    path('edit/<int:pk>', app.views.edit, name='edit'),
    path('delete/<int:pk>', app.views.delete, name='delete'),
    
    path('comment/<int:pk>', app.views.comment, name='comment'),
    path('comment_edit/<int:pk>', app.views.comment_edit, name='comment_edit'),
    path('comment_delete/<int:pk>', app.views.comment_delete, name='comment_delete'),
    
    path('like/<int:pk>', app.views.like, name='like'),
    
    path('user/<str:pk>', app.views.user, name='user'),
    path('news/', app.views.news, name='news'),
    path('follow/<int:fk>', app.views.follow, name='follow'),
    path('unfollow/<int:fk>', app.views.unfollow, name='unfollow'),
    path('search', app.views.search, name='search'),
    
    path('hashtag/<int:pk>', app.views.hashtag, name='hashtag'),
    
    path('signin', app.views.signin, name='signin'),
    path('signup', app.views.signup, name='signup'),
    
    path('error', app.views.error, name='error'),
   
    path('count', count.views.count_home, name="count_home"),
    path('diary', diary_home.as_view()),
    #Auth에서 제공해주는 기능쓰기
    path('app/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
