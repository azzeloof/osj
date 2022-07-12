from django.shortcuts import render, get_object_or_404
import articles
from osj.views import getUserContext


def allArticles(request):
    articleObjs = articles.models.Article.objects.all()
    context = {
        'articles': articleObjs
    }
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'articles/allArticles.html', context)


def article(request, objID):
    articleObj = get_object_or_404(articles.models.Article, id=objID)
    context = {
        'article': articleObj
    }
    if request.user.is_authenticated:
        context.update(getUserContext(request))
    return render(request, 'articles/article.html',context)
