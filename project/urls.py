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
import app.views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.home, name="home"),
    path('edit/<int:pk>', app.views.edit, name='edit'),
    path('delete/<int:pk>', app.views.delete, name='delete'),
    
    path('comment/<int:pk>', app.views.comment, name='comment'),
    path('comment_edit/<int:pk>', app.views.comment_edit, name='comment_edit'),
    path('comment_delete/<int:pk>', app.views.comment_delete, name='comment_delete'),
    
    path('user/<str:pk>', app.views.user, name='user'),
    path('hashtag/<int:pk>', app.views.hashtag, name='hashtag'),
    
    path('signin', app.views.signin, name='signin'),
    path('signup', app.views.signup, name='signup'),
    
    #Auth에서 제공해주는 기능쓰기
    path('app/', include('django.contrib.auth.urls')),
    
]
