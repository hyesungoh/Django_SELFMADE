from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, Hashtag
from .forms import PostForm, CommentForm, HashtagForm, LoginForm, UserForm

# SIGN IN, OUT
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

def home(request):
    posts = Post.objects
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.date = timezone.now()
            post.writer = request.user
            
            # '#'을 기준으로 해시태그 만들기 !
            tags = form.cleaned_data['hashtag']
            str_tags = tags.split('#')
            list_tags = list()
            for tag in str_tags:
                hashtag = HashtagForm().save(commit=False)
                # 이미 만들어진 해시태그인지 검사
                if Hashtag.objects.filter(name=tag):
                    list_tags.append(Hashtag.objects.get(name=tag))
                else:
                    hashtag.name = tag
                    hashtag.save()
                    list_tags.append(hashtag)
            
            post.save()
            post.hashtags.add(*list_tags)
            
            # 이걸 따로 할 필요가 있을까?
            # form.save_m2m()
            return redirect('home')
    else:
        form = PostForm()
        c_form = CommentForm()
        return render(request, 'app/home.html', {'form': form, 'c_form': c_form, 'posts': posts})

def edit(request, pk):
    edit_post = get_object_or_404(Post, pk=pk)

    # csrf 방지
    if edit_post.writer != request.user:
        return HttpResponse('You can edit your own post')
        
    posts = Post.objects
    if request.method == 'POST':
        form = PostForm(request.POST, instance=edit_post)
        if form.is_valid():
            post = form.save(commit=False)
            post.date = timezone.now()
            post.writer = request.user
            
            tags = form.cleaned_data['hashtag']
            str_tags = tags.split('#')
            list_tags = list()
            for tag in str_tags:
                hashtag = HashtagForm().save(commit=False)
                if Hashtag.objects.filter(name=tag):
                    list_tags.append(Hashtag.objects.get(name=tag))
                else:
                    hashtag.name = tag
                    hashtag.save()
                    list_tags.append(hashtag)

            post.save()
            post.hashtags.add(*list_tags)
            return redirect('home')
    else:
        form = PostForm(instance=edit_post)
        return render(request, 'app/edit.html', {'e_p': edit_post.id ,'form': form, 'posts': posts})
        
        
        
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
    

def comment_edit(request, pk):
    edit_comment = get_object_or_404(Comment, pk=pk)
    posts = Post.objects

    # csrf 방지
    if edit_comment.c_writer != request.user:
        return HttpResponse('You can edit your own comment')

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=edit_comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.text = form.cleaned_data["text"]
            comment.save()
            return redirect('home')
    else:
        form = CommentForm(instance=edit_comment)
        return render(request, 'app/comment_edit.html', {'e_c': edit_comment.id ,'form': form, 'posts': posts})

    
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.c_writer == request.user:
        comment.delete()
        return redirect('home')
    else:
        return HttpResponse('You can delete your own post')
    
# def hashtag(request, hashtag=None):
#     if request.method == 'POST':
#         form = HashtagForm(request.POST, instance=HashtagForm)
#         if form.is_valid():
#             hashtag = form.save(commit=False)
#             if Hashtag.objects.filter(name=form.cleaned_data['name']):
#                 form = HashtagForm()
#                 error_message = "Already"
#                 return render(request, 'app/hashtag.html', {'form': form, 'e_m': error_message})
#             else:
#                 hashtag.name = form.cleaned_data['name']
#                 hashtag.save()
#             return redirect('home')
#     else:
#         form = HashtagForm(instance=hashtag)
#         return render(request, 'app/hashtag.html', {'form': form})

def user(request, pk):
    user = User.objects.get(username=pk)
    posts = Post.objects.filter(writer=user)
    c_form = CommentForm()
    return render(request, 'app/user.html', {'user': user, 'posts': posts, 'c_form': c_form})

def hashtag(request, pk):
    hashtag = Hashtag.objects.get(id=pk)
    posts = Post.objects.filter(hashtags=hashtag)
    return render(request, 'app/hashtag.html', {'hashtag': hashtag, 'posts': posts})

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