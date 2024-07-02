from django.shortcuts import render, redirect
from .models import Article, Comment
from .forms import CommentForm, UserCreationForm, LoginForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as django_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.backends import ModelBackend
from .permissions import check_is_creator_or_admin

# Create your views here.
# Article.objects.create(
#     title = "세션하는 날",
#     content = "나 천재인가? 이걸 이렇게 잘할 수 있다니",
# )

# Article.objects.all()

# Article.objects.get(pk=2)

get_user_model().objects.filter(username="admin").exists()

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            django_login(request, user)
            return redirect("home")
        else:
            print(form.errors)
    else:
        form = UserCreationForm()

    return render(request, "signup.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("home")
    else:
        return redirect("login")

@login_required
def new(request):
    categories = Article.category_choices
    if request.method == 'POST':
        print(request.POST)
        new_article = Article.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            category = request.POST['category'],
        )
        return redirect('list')
    return render(request,'new.html', {'categories': categories})

def list(request):
    categories = Article.category_choices
    articles=Article.objects.all()
    categories_with_counts = []
    for category_id, category_name in categories:
        count = Article.objects.filter(category=category_id).count()
        categories_with_counts.append((category_id, category_name, count))
    return render(request,'list.html',{'articles':articles, 'categories_with_counts': categories_with_counts})

def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    comments = article.comments.filter(parent=None)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_id = request.POST.get('parent')
            parent_comment = None
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
            Comment.objects.create(
                article=article,
                content=form.cleaned_data['content'],
                parent=parent_comment
            )
            return redirect('detail', article_id=article_id)
    else:
        form = CommentForm()
    return render(request, 'detail.html', {'article': article, 'comments': comments, 'form': form})

def category(request, category_id):
    articles=Article.objects.filter(category=category_id)
    return render(request, 'category.html', {'articles': articles})

@login_required
@check_is_creator_or_admin(Article, 'article_id')
def delete(request, article_id):
    article = Article.objects.get(id=article_id)
    article.delete()
    
    return redirect('list')

@login_required
@check_is_creator_or_admin(Comment, 'comment_id')
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    article_id = comment.article.id
    comment.delete()
    return redirect('detail', article_id)

@login_required
@check_is_creator_or_admin(Article, 'article_id')
def edit(request, article_id):
    article = Article.objects.get(id=article_id)
    categories = Article.category_choices
    
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        Article.objects.filter(id=article_id).update(title=title, content=content, category=category)
        return redirect('detail', article_id)
    return render(request, 'edit.html', {'article': article, 'categories': categories})

def base(request):
    return render(request, 'base.html')