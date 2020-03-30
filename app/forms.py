from django import forms
from .models import Post
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']
        
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']