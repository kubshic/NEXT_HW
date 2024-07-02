from django.shortcuts import render, redirect
from .models import Post
from django.utils import timezone
# from django.utils.timezone import now

# Create your views here.

def home(request):  
    posts = Post.objects.all().order_by('deadline')
    
    for post in posts:
        time_left = post.deadline - timezone.now()
        if time_left.days +1 < 0:
            post.dday = f"+{-(time_left.days+1)}"
        elif time_left.days +1 > 0:
            post.dday = ( time_left.days+1) * (-1)
        else:
            post.dday = "-Day"
            
    return render(request, 'home.html', {'posts':posts})
    

def new(request):
    if request.method == 'POST':
        new_post = Post.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            deadline = request.POST['deadline']
        )
        return redirect('detail', new_post.pk)
    
    return render(request, 'new.html')

def detail(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    
    return render(request, 'detail.html', {'post': post})

def update(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    
    if request.method == 'POST':
        Post.objects.filter(pk=post_pk).update(
            title = request.POST['title'],
            content = request.POST['content'],
            deadline = request.POST['deadline'],
        )
        return redirect('detail', post_pk)
    
    return render(request, 'update.html', {'post': post})

def delete(request, post_pk):
    post = Post.objects.get(pk=post_pk)
    post.delete()
    
    return redirect('home')