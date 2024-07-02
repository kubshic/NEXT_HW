from django.contrib import admin
from .models import Article
from .models import Comment
from django.contrib.auth import get_user_model



User = get_user_model()
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(User)