from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json

from .models import Comment, Post, Like


def signup(request):
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      exist_user = User.objects.filter(username=username)
      if exist_user:
           error = "이미 존재하는 유저입니다."
           return render(request, 'registration/signup.html', {"error":error})
      
      new_user = User.objects.create_user(username=username, password=password)
      auth.login(request, new_user)
   
      return redirect('home')
       
   return render(request, 'registration/signup.html')

def login(request):
   if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      user = auth.authenticate(username=username, password=password)
      if user is not None:
           auth.login(request, user)
           return redirect(request.GET.get('next', '/'))
      error = "아이디 또는 비밀번호가 틀립니다"
      return render(request, 'registration/login.html', {"error":error})
        
   return render(request, 'registration/login.html')

def home(request):
   posts = Post.objects.all()

   return render(request, 'home.html', {'posts':posts})


def logout(request):
   auth.logout(request)
   return redirect('home')

@login_required(login_url="/registration/login/")
def new(request):
   if request.method == "POST":
       title = request.POST['title']
       content = request.POST['content']


       new_post = Post.objects.create(
           title=title,
           content=content,
           author=request.user
           )
       return redirect('detail', new_post.pk)
  
   return render(request, 'new.html')

@login_required(login_url="/registration/login/")
def detail(request, post_pk):
   post = Post.objects.get(pk=post_pk)
   if (request.method == 'POST'):
      Comment.objects.create(
         post=post,
         content=request.POST['content'],
         author=request.user
      )
      return redirect('detail', post_pk)
   return render(request, 'detail.html', {'post': post})



def edit(request, post_pk):
   post = Post.objects.get(pk=post_pk)


   if request.method == 'POST':
       title = request.POST['title']
       content = request.POST['content']
       Post.objects.filter(pk=post_pk).update(
           title=title,
           content=content
       )
       return redirect('detail', post_pk)


   return render(request, 'edit.html', {'post':post})


def delete(request, post_pk):
   post = Post.objects.get(pk=post_pk)
   post.delete()
   return redirect('home')

@csrf_protect
@login_required(login_url="/registration/login/")
def submit_comment(request):
    if request.method == 'POST':
        try:
            request_body = json.loads(request.body)
            post_pk = request_body.get('post_pk')
            content = request_body.get('content')
            post = get_object_or_404(Post, pk=post_pk)
            
            new_comment = Comment.objects.create(
                post=post,
                content=content,
                author=request.user
            )
            response = {
                'comment_content': new_comment.content,
                'comment_author': new_comment.author.username,
                'post': post_pk,
            }
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def delete_comment(request, post_pk, comment_pk):
   comment = Comment.objects.get(pk=comment_pk)
   comment.delete()
   return redirect('detail', post_pk)

@csrf_exempt
def like(request, post_pk):
   if request.method == 'POST':
      request_body = json.loads(request.body)
      post_pk = request_body['post_pk']
      post = Post.objects.get(pk=post_pk)
      user_like = Like.objects.filter(user=request.user, post=post)
      
      if (len(user_like) > 0):
         user_like.delete()
      else:
         Like.objects.create(
            post=post,
            user=request.user
         )
      response = {
         'like_count': post.likes.count(),
      }
      return HttpResponse(json.dumps(response))