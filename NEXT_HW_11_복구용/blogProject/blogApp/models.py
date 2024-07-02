from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
# 우리가 만드는 모델들은 장고가 미리 만들어둔 models.Model이라는 class를 상속

# pk는 따로 명시하지 않아도 됨! 장고는 ok를 자동으로 생성하여 1부터 순서대로 번호를 붙여준다.
# class 를 사용하여 테이블의 schema를 정의
# 새로운 클래스(자식)를 생성할 때, 기존에 정의되어 있는 다른 클래스(부모)의 특성들을 물려받음
# Article 모델은 models.Model의 특성들을 기본으로 가진다.
class Article(models.Model):
    title = models.CharField(max_length=200)
    # CharField - 작은 string부터 큰 string까지 입력
    content = models.TextField()
    # TextField - 큰 string을 입력
    category_choices = [
        ('option1', '취미'),
        ('option2', '음식'),
        ('option3', '프로그래밍'),]
    category = models.TextField(choices=category_choices, default='option1')
    time = models.DateTimeField(auto_now_add=True, null=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles"
    )
    
    # __str__: 위에서 우리가 만든 Article 모델로 만든 오브젝트 자체를 출력할 때 값을 title로 할래!
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    def __str__(self):
       return self.content

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, username, password):
        if not username:
            raise ValueError('must have username')
        if not password:
            raise ValueError('must have password')
    
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    username = models.CharField(max_length=255, unique=True)
    UWERNAME_FIELD = "username"
    def __str__(self) -> str:
        return self.username