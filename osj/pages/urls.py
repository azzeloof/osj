from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('page/<str:slug>', views.page, name='page'),
    path('about/', views.page, {'slug':'about'}, name='about'), # Special case for About page
    path('jewelry/', views.allJewelry, name='jewelry'),
    path('articles/', views.allArticles, name='articles'),
    path('jewelry/<int:objID>', views.jewelryPiece, name='jewelryPiece'),
    path('articles/<int:objID>', views.article, name='article'),
    path('jewelry/new', login_required(views.JewelryCreateView.as_view()), name='newJewelry'),
    path('jewelry/<pk>/edit', login_required(views.JewelryUpdateView.as_view()), name='editJewelry'),
    #re_path(r'^$',views.like_button, name='like'),
    path('like/', views.like_button, name='like'),
    path('tagged/<str:slug>', views.tagged, name='tagged'),
    path('tagged/', views.tagged, name='tagged')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
