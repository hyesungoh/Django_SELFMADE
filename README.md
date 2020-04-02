## 군대 사지방에서하는 Django 공부 !!

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

___
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