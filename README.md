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

