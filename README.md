## 군대 사지방에서하는 Django 공부 !!

#### 2020.03.30
##### create, read, update 기능 구현
##### Sign in, up, out 구현
###### 다음에 할 것 : 1:N 관계를 이용한 POST와 USER, POST와 COMMENT 구현하기

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
