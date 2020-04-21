from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post, Comment, Hashtag, Relationship
from .forms import PostForm, CommentForm, HashtagForm, LoginForm, UserForm

# SIGN IN, OUT
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
    posts = Post.objects
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
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

def news(request):
    if not request.user.is_active:
        return HttpResponse('First SignIn please')
    
    r_user = request.user
    rela = Relationship.objects.filter(who=r_user)
    posts = list()
    for whom in rela:
        u = User.objects.get(username=whom.whom)
        p = Post.objects.filter(writer=u)
        for post in p:
            posts.append(post)

    posts.sort(key=lambda x: x.date, reverse=True)

    c_form = CommentForm()
    return render(request, 'app/news.html', {'posts': posts, 'c_form': c_form})
    
def edit(request, pk):
    edit_post = get_object_or_404(Post, pk=pk)

    # csrf 방지
    if edit_post.writer != request.user:
        return HttpResponse('You can edit your own post')
        
    posts = Post.objects
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=edit_post)
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
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = PostForm(instance=edit_post)
        return render(request, 'app/edit.html', {'e_p': edit_post.id, 'form': form, 'posts': posts})
        
        
        
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.writer == request.user:
        post.delete()
        # return redirect('home')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
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
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

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
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = CommentForm(instance=edit_comment)
        return render(request, 'app/comment_edit.html', {'e_c': edit_comment.id ,'form': form, 'posts': posts})

    
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.c_writer == request.user:
        comment.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('You can delete your own post')

def like(request, pk):
    if not request.user.is_active:
        return HttpResponse('First SignIn please')
    
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
def user(request, pk):
    user = User.objects.get(username=pk)
    posts = Post.objects.filter(writer=user)
    c_form = CommentForm()
    
    r = Relationship.objects
    # flw, flwing 명단을 확인하기 위해
    flw_list = r.filter(who=user)
    flwer_list = r.filter(whom=user)
    flw = flw_list.count()
    flwer = flwer_list.count()

    if request.user.is_authenticated:
        # 현재 Signin한 user의 Follow 유무를 위해
        b = r.filter(who=request.user, whom=user)

        return render(request, 'app/user.html', {'b': b,'flw': flw, 'flwer': flwer, 'flw_list': flw_list, 'flwer_list': flwer_list, 'user': user, 'posts': posts, 'c_form': c_form})
    else:
        return render(request, 'app/user.html', {'flw': flw, 'flwer': flwer, 'flw_list': flw_list, 'flwer_list': flwer_list, 'user': user, 'posts': posts, 'c_form': c_form})

def follow(request, fk):
    who = request.user
    whom = User.objects.get(id=fk)
    r = Relationship()
    r.who = who
    r.whom = whom
    r.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unfollow(request, fk):
    who = request.user
    whom = User.objects.get(id=fk)
    Relationship.objects.get(who=who, whom=whom).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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