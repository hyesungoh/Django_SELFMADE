## 군대 사지방에서하는 Django 공부 !!
### 목표 : INSTAGRAM ~~***(backend)***~~
___
#### 2020.03.30
##### create, read, update 기능 구현
##### Sign in, up, out 구현
###### 다음에 할 것 : 1:N 관계를 이용한 POST와 USER, POST와 COMMENT 구현하기

___
#### 2020.03.31
##### Post와 User 1:N 관계 형성
###### Sign In한 사람만 글 작성 가능 > 글 작성시 writer 표시

```python
You are trying to add a non-nullable fiel
# 이거랑
no such column

# 위 오류로 인해 1시간 삽질
# non-nullable은 default=""를 부여해서 해결

# python manage.py flush로 데이터 삭제를 할 수 있다는 걸 배움

# no such 오류는 migration의 오류라 프로젝트 clone 받아서 고침^^
```
###### 다음에 할 것 : POST와 COMMENT 연결 및 구현하기

#### 2020.04.01
##### Post와 Comment의 연결 성공
##### 한 template(home)에서 글 작성, 댓글 작성, 글 수정을 가능하게 하려해서 막힘
##### superuser를 사용하여 model 관계는 잘된다는 것을 확인함
###### 다음에 할 것 : home template에서 댓글 작성 가능하게 할 것

___
#### 2020.04.02
##### Home template에서 글 작성, 글 수정, 댓글 작성 가능!!

```html
<!-- home.html -->
<form method='POST' action='/comment/{{ post.id }}'>
            {% csrf_token %}
            <table>
                {{ c_form.as_p }}
            </table>
            <input type='submit', value='submit'>
        </form>
```
##### form 태그의 action에 post.id를 넘겨줌
```python
# views.py
def commenting(request, pk):
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

```
##### views에서 저장 후, redirect를 home으로 하여 한 template에서 한 것처럼 보이게 함

###### 다음에 할 것 : 글, 댓글 작성 유저와 Signin한 유저가 같을 시 글, 댓글 삭제하기 !!

___
#### 2020.04.05
##### 글과 댓글의 작성자가 현재 SignIn한 User와 같을 시 삭제 및 수정이 가능함
###### 댓글은 삭제만

##### csrf 같이 주소를 직접쳐서 들어가면 삭제가 되어 views와 home.html에서 두 번 확인
```python
# Post 작성자가 현재 SignIn한 User와 같은 지 확인
if post.writer == request.user:
```
```html
<!-- Comment 작성자가 현재 SignIn한 User와 같은 지 확인-->
{% if comment.c_writer == request.user %}
```
###### 다음에 할 것 : 댓글 수정, Post에 Hashtag 추가

___
#### 2020.04.06
##### 댓글 수정이 가능함
##### home view에서 모든 동작을 처리하는 것에서 edit(post), comment_edit view를 만들어 나누어서 처리하는 형식으로 바꿈
###### edit에서는 새로운 글쓰기 제한, comment_edit에서는 새로운 댓글 및 삭제 제한 등 다른 점을 부여함

```html
<!-- edit.html / 'e_p': edit_post  -->
{% for post in posts.all %}
    {% if post.id == e_p %}
```
##### 위와 같이 순서에 맞는 글, 댓글 공간에 form을 둘 수 있게 됨

```python
# views.py > def edit
if edit_post.writer != request.user:
    HttpResponse('You can edit your own post')
```
##### csrf 방지를 위해 위 문법을 사용했는데 ~~방금 작동하지 않는 걸 확인 함ㅋ~~
##### HttpResponse에 break같은 기능이 없는 것으로 추정됨
###### 다음에 할 것 : views.py > def edit, comment_edit에 csrf 방지하기, Post에 Hashtag 추가하기

___
#### 2020.04.07
```python
# views.py > def edit
if edit_post.writer != request.user:
    return HttpResponse('You can edit your own post')
```
##### HttpResponse는 앞에 return을 안붙여서 생긴 해프닝이였다 ㅋ

```python
# views.py > def home / '#'을 기준으로 해시태그 만들기 !
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
```

##### Post와 Hashtag M:N 관계 형성 완료
###### Post에 CharField hashtag와 ManyToManyField hashtags를 추가 후
###### template에서 hashtag만 입력받으며 view에서 #을 기준으로 hashtag를 split하고 각 객체마다 list에 append하고 hashtags에 add함
##### views.py > def edit도 똑같이 적용
###### 다음에 할 것 : hashtag와 user template 만들기 ! (hashtag, user별 post보기)

___
#### 2020.04.08
##### Hashtag와 User의 개인 Template 구현 완료
```python
# views.py / def user는 댓글 작성도 가능하게 구현
def user(request, pk):
    user = User.objects.get(username=pk)
    posts = Post.objects.filter(writer=user)
    c_form = CommentForm()
    return render(request, 'app/user.html', {'user': user, 'posts': posts, 'c_form': c_form})

def hashtag(request, pk):
    hashtag = Hashtag.objects.get(id=pk)
    posts = Post.objects.filter(hashtags=hashtag)
    return render(request, 'app/hashtag.html', {'hashtag': hashtag, 'posts': posts})
```
##### Model.object.filter method를 사용하여 간편했음

```html
<!-- user template로 가기-->
<a href="{% url 'user' pk=user.username %}">{{ user.username }}</a>

<!-- hashtag template로 가기-->
<a href="{% url 'hashtag' pk=hashtag.id %}">
    <span>{{ hashtag.name }}</span>
</a>
```
##### App의 자연스러운 flow를 위해서 적재적소에 a 태그를 배치
###### 다음에 할 것 : Image Uploader 구현 및 Post에 Img 포함
###### User Profile Img / User Follow, Following / Follow한 User의 Post만 보기
###### ~~User Model을 갈아엎어야하나 .. DB 설계가 중요하다는 것을 다시 깨달음~~

___
#### 2020.04.09
##### Post model에 Image 추가 / image upload와 확인 가능
###### RubyOnRails와 다르게 동일 이름의 img를 upload한 상황을 알아서 해결해줌
```python
# settings.py / static과 media의 root, url 설정
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# views.py > def home
form = PostForm(request.POST, request.FILES)
```
```html
<form method='POST' enctype="multipart/form-data">
```
##### img upload를 위해 추가 및 수정해준 것들

###### 다음에 할 것 : User 모델 Custom (follow, following)

___
#### 2020.04.13
##### User간 Follow, Unfollow 가능 및 확인 가능
```python
# models.py
class Relationship(models.Model):
    who = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="who", on_delete=models.CASCADE)
    whom = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="whom", on_delete=models.CASCADE)
    
# views.py
def follow(request, fk):
    who = request.user
    whom = User.objects.get(id=fk)
    r = Relationship()
    r.who = who
    r.whom = whom
    r.save()
    return redirect('home')

def unfollow(request, fk):
    who = request.user
    whom = User.objects.get(id=fk)
    Relationship.objects.get(who=who, whom=whom).delete()
    return redirect('home')  
```
##### User Model을 Custom하지 않고 관계형 Model을 만들어서 함
##### Follow 함수에서 Unfollow 기능까지 구현할까 하다 Template에서 Follow 혹은 Unfollow 확인을 위해 위처럼 함

```python
# views.py > def user
    r = Relationship.objects
    # flw, flwing 명단을 확인하기 위해
    flw_list = r.filter(who=user)
    flwer_list = r.filter(whom=user)
    flw = flw_list.count()
    flwer = flwer_list.count()

    # 현재 Signin한 user의 Follow 유무를 위해
    b = r.filter(who=request.user, whom=user)
```

```html
<!-- user.html -->
<h1>This is {{user.username}}'s home</h1>
<p>follow : {{ flw }}</p>
{% for f in flw_list %}
{{ f.whom }}
{% endfor %}

<p>following : {{ flwer }}</p>
{% for f in flwer_list %}
{{ f.who }}
{% endfor %}
```
##### Template에서 Model.objects.filter(), count()등 method가 동작하지 않아 views에서 넘겨주는 변수들이 많음
###### 그렇다고 Template에서 모든 Relationship을 반복하며 확인하는 것은 비효율적이라 생각함
##### 다음에 할 것 : Post에 좋아요 기능, SignIn 안됐을 시 User Template, redirect를 왔던 곳으로 보내기?

___
#### 2020.04.15
##### SignIn 안됐을 시 User template 오류 해결, redirect to previous page 가능
```python
# views.py
if request.user.is_authenticated:
    b = r.filter(who=request.user, whom=user)
    return render ~~~
else:
    return render ~~~ (without b)
```
##### 현재 SignIn이 되었는 지 확인을 통해 Follow, Unfollow a태그 조절
```python
# views.py
from django.http import HttpResponse, HttpResponseRedirect

return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
```
##### 위 코드를 통해 이전 페이지로 redirect 가능
##### 다음에 할 것 : Post에 좋아요 기능, SignIn 시 Follow한 User의 Post만 보여주기

___
#### 2020.04.16
##### Post에 Like 가능
```python
# models.py
class Post(models.Model):
    ...
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes")
    
# views.py
def like(request, pk):
    # SignIn 확인
    if not request.user.is_active:
        return HttpResponse('First SignIn please')
    
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    
    # 현재 Like 상태 확인
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)
    
    # 이전 페이지로 redirect
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# urls.py
path('like/<int:pk>', app.views.like, name='like')
```
```html
<!-- Posts 반복문 중 -->
<p>{{ post.likes.count }} / <a href="{% url 'like' pk=post.pk %}">like</a></p>
```
###### 다음에 할 것 : Template 상속으로 조금 더 유연하게 만들기, 뉴스피드 만들기

___
#### 2020.04.19
##### Newsfeed 구현 (팔로우한 User의 Post만 보여주는 단계)
```python
# views.py 
def news(request):
    # SignIn 여부 확인
    if not request.user.is_active:
        return HttpResponse('First SignIn please')
    
    r_user = request.user
    rela = Relationship.objects.filter(who=r_user)
    posts = list()
    for whom in rela:
        # 내가 Follow한 User
        u = User.objects.get(username=whom.whom)
        # 그 User가 작성자인 Post.objects
        p = Post.objects.filter(writer=u)
        # p가 Post.objects이기 때문에
        for post in p: 
            posts.append(post)
            
    c_form = CommentForm()
    return render(request, 'app/news.html', {'posts': posts, 'c_form': c_form})
```
##### 다음에 할 것 : Newsfeed에 Order_by 작성일, Template 상속

___
#### 2020.04.21
##### Home, Newsfeed 정렬 구현 (order_by, list.sort())
```python
# views.py > def news
# posts = list('post_object', 'post_object', 'post_object', ...)
posts.sort(key=lambda x: x.date, reverse=True)

# views.py > def home
posts = Post.objects.all().order_by('-date')
```
##### 다음에 할 것 : Template 상속, Front end? User custom? 다시 만들기?

___
#### 2020.04.22
##### 부모, 자식 Template 연결 성공
```python
# settings.py
'DIRS': [os.path.join(BASE_DIR, 'templates')],

# in html
{% extends "app/base.html" %}
```
###### 주소 오류로 30분을 소비한 내가 밉다
##### 부모 Template의 모든 것을 자식 template가 상속받아야 하고 html에 뿌려줘야 한다는 것을 몰랐음
###### project 디자인적으로나 template extends에 관해서 무지했음
##### 다음에 할 것 : base.html 수정 > home, hashtag, user template에만 상속시켜주면 될 듯

___
#### 2020.04.23
##### Bootstrap Theme 적용
##### Home, User template에 적용 완료
```python
# settings.py
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```
###### The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting.
##### 위 Issue로 인해 STATIC_ROOT 주석처리
##### 다음에 할 것 : Hashtag Template에 적용하기, base.html에 posts block, nav block 보기좋게 조정하기

___
#### 2020.04.27
##### base.html에 Nav, Footer block 약간 수정
##### Hashtag Template 적용 완료
##### 다음에 할 것 : Nav Block에 User home 추가하기, User 검색 기능 추가하기

___
#### 2020.04.28
##### User Search 기능 구현
```html
<!-- base.html > nav block -->
<li class="nav-item">
    <form action="{% url 'search' %}" method="GET">
        <input type="search" name="name">
        <input type="submit" value="submit">
    </form>
</li>
```

```python
# views.py
def search(request):
    name = request.GET["name"]
    if name:
        users = User.objects.filter(username__contains=name)
    return render(request, 'app/search.html', {'users': users, 'name': name})

```
###### url상 pk, fk가 아닌 request.GET으로 값을 받아올 수 있는지 몰랐다..
##### base.html에 posts block을 빼고 nav와 footer만 남겨둠
###### 용도에 맞게 모든 template에 적용하기 위함

___
#### 2020.04.30
##### base.html의 user a tag 오류 수정
```html
<!-- <a class="nav-link" href="{% url 'user' pk=user.username%}">{{ user.username }}</a>
User template 들어가면 그 유저로 보였음-->

<a class="nav-link" href="{% url 'user' pk=user.username%}">{{ request.user.username }}</a>
```
###### news template를 위한 nav li 작성, search template 디자인 조정함
##### 다음에 할 것 : Post 작성과 수정을 위한 Url을 개설할까? EDIT 방식은 수정이 필요함 > 글 작성까지 새로 만들면 더 깔끔할 듯

___
#### 2020.05.03
##### Edit Template 다시 구현 (Edit할 포스트만 보여주기)
###### base.html도 extends함
##### 다음에 할 것 : Post 작성도 다시 구현, Bootstrap form with django?

___
#### 2020.05.07
##### Post 작성 기능을 Write view와 template으로 기능하게 함
###### nav와 home에서 write url로 이동 가능
##### Django model form class 적용 방법을 배움
```python
# forms.py
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image', 'hashtag']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'hashtag': forms.TextInput(attrs={'class': 'form-control'})
        }
```
##### 다음에 할 것 : form 디자인 조금 더 / HttpResponse도 꾸밀 수 있나?

___
#### 2020.05.11
##### 기존 return httpresponse를 error view를 불러오는 것으로 대체
```python
# views.py

def something(request):
    ...
    return error(request, "You can write a post with SIGNIN")

def error(request, error_msg):
    return render(request, 'app/error.html', {'error_msg': error_msg})
```
###### 이렇게하여 error page에 base.html 상속등 디자인을 할 수 있게 됨
##### 다음에 할 것 : edit template design

___
#### 2020.05.12
##### Edit template를 write template와 똑같이 디자인
##### Post Edit간에 hashtag를 수정할 떄 기존 hashtag가 유지되는 Issue 발생
```python
# views.py > def edit
    post.hashtags.clear()
```
###### 위 method를 사용하여 간단히 해결
##### 다음에 할 것 : SignIn, Up template design?

___
#### 2020.05.13
##### SignIn, SignUp template 새롭게 디자인
###### forms.py에 UserForm widgets를 활용했는데 SignUp에만 먹는 이슈 존재
```html
{{ form.as_p }}
<!-- 위처럼 한 번에 뿌려주는 것 외에 -->
{{ form.username }}
<!-- 이렇게 할 수 있다는 것을 배움 -->
```

___
#### 2020.05.14
##### comment_edit template를 base.html 상속하여 새롭게 디자인
###### 기존 모든 post와 모든 comment들을 보여주는 방식에서 수정하는 댓글이 달린 post와 수정 할 comment를 form으로 보여줌
```python
# views.py > def comment_edit
    post = Post.objects.get(comments = edit_comment)
    # comment.id를 가지고 post를 찾는데 거창한 코드가 필요없어서 놀람
```
##### 다음에 할 것 : 다른 프로젝트를 만들기는 귀찮으니 이 프로젝트에 새로운 기능을 구현해볼까? 예를 들면 전역일까지 시간계산기

___
#### 2020.05.19
##### count app 새로 만듦
```python
# settings.py
INSTALLED_APPS = [
    'count.apps.CountConfig',
    ...
]

# urls.py
urlpatterns = [
    path('count', count.views.count_home, name="count_home"),
    ...
]
```
###### 서비스를 여러 개의 app으로 만드는 버릇을 들이자
```python
# count/views.py
from datetime import datetime

def count_home(request):
    ...
    date_format = "%Y-%m-%d"
    start_day = datetime.strptime(request.POST["start_day"], date_format) 
        end_day =datetime.strptime(request.POST["end_day"], date_format)
        present_day =datetime.strptime(request.POST["present_day"], date_format)

        remain_days = end_day - present_day
        ...
```
##### datetime을 이용하여 간단하게 남은 일 수를 계산해봄
##### 다음에 할 것 : 남은 일 수 %로 보여주기 등 하고싶은 대로 만들어보자

___
#### 2020.05.20
##### count/home에 총 날짜, 한 날짜, 남은 날짜, 한 날짜 퍼센트로 볼 수 있음
```python
# count/views.py
def count_home(request):
    ...
    total_days = end_day - start_day
    remain_days = end_day - present_day
    ran_days = present_day - start_day
    ran_percent = (ran_days / total_days) * 100
    
    # datetime.timedelta 객체의 쉬운 사칙연산 지원으로 간단히 만듦
    ...
```
##### 다음에 할 것 : aws ec2 배포를 공부해야 함, app에서 count 기능도 사용할 수 있게끔?

___
#### 2020.05.25
##### app/base.html에 count로 가는 li 추가
##### 다음에 할 것 : aws ec2 배포 공부 > 따라해보고 싶은데 휴대폰을 사용해야함 ㅠ

___
#### 2020.05.26
##### github를 이용한 협업 방식 중 fork를 이용하여 중앙 upstream에 pull request하는 방식이 좋아보인다.
###### 이번 프로젝트에 사용하고 싶지만 전체적으로 따라오기 쉬울까 걱정, 쉬운 건 현재 사용중인 구름ide가 짱이긴 한데
##### 다음에 할 것 : app을 하나 더 만들어서 기능을 나눠보자, 크롤링 기능은 어떨까