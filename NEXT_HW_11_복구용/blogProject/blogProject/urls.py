"""
URL configuration for blogProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blogApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('new/', views.new, name='new'),
    path('list/', views.list, name='list'),
    path('detail/<int:article_id>', views.detail, name='detail'),
    # detial 뒷부분 매개변수. 매개변수의 형태 int 정수. view.detail에게 넘길 때 article_id라는 이름으로 줄게!
    path('category/<str:category_id>', views.category, name='category'),
    path('delete/<int:article_id>', views.delete, name='delete'),
    path('delete-comment/<int:article_id>/<int:comment_id>', views.delete_comment, name='delete-comment'),
    path('base', views.base, name='base'),
]
