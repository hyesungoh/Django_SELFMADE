from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm, CommentForm, LoginForm, UserForm

# SIGN IN, OUT
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

# Create your views here.
# def postform(request, post=None):
#     if request.method == 'POST':
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.date = timezone.now()
#             post.save()
#             return redirect('home')
#     else:
#         form = PostForm(instance=post)
#         return render(request, 'app/home.html', {'form':form})

def home(request, post=None, comment=None):
    posts = Post.objects
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        comment_form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            post = form.save(commit=False)
            post.date = timezone.now()
            post.writer = request.user
            post.save()
            return redirect('home')
        
    else:
        form = PostForm(instance=post)
        c_form = CommentForm(instance=comment)
        return render(request, 'app/home.html', {'form': form, 'c_form': c_form, 'posts': posts})
    # return render(request, 'app/home.html', {'posts': posts})

def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.writer == request.user:
        return home(request, post)
    else:
        return HttpResponse('You can edit your own post')

def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.writer == request.user:
        post.delete()
        return redirect('home')
    else:
        return HttpResponse('You can delete your own post')
    
def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post
            comment.text= form.cleaned_data["text"]
            comment.c_writer = request.user
            comment.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
        c_form = CommentForm(instance=comment)
        return render(request, 'app/home.html', {'form': form, 'c_form': c_form, 'posts': posts})

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Fail to signin')
    else:
        form = LoginForm()
        return render(request, 'app/signin.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username = form.cleaned_data["username"], email=form.cleaned_data["email"], password=form.cleaned_data["password"])
            login(request, new_user)
            return redirect('home')
        else:
            return HttpResponse('Fail to Signup')
    else:
        form = UserForm()
        return render(request, 'app/signup.html', {'form': form})