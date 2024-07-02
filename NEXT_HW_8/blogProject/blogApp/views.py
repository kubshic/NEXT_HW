from django.shortcuts import render, redirect
from .models import Article

# Create your views here.
# Article.objects.create(
#     title = "세션하는 날",
#     content = "나 천재인가? 이걸 이렇게 잘할 수 있다니",
# )

# Article.objects.all()

# Article.objects.get(pk=2)

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
    return render(request, 'detail.html', {'article': article})

def category(request, category_id):
    articles=Article.objects.filter(category=category_id)
    return render(request, 'category.html', {'articles': articles})