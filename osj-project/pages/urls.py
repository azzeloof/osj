from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('legal/<str:slug>/', views.legal, name='legal'),
    path('page/<str:slug>/', views.page, name='page'),
    path('about/', views.page, {'slug':'about'}, name='about'), # Special case for About page
    #path('jewelry/', views.allJewelry, name='jewelry'),
    path('jewelry/', views.JewelryListView.as_view(), name='jewelry'),
    path('articles/', views.allArticles, name='articles'),
    #path('jewelry/<int:objID>', views.jewelryPiece, name='jewelryPiece'),
    path('jewelry/<int:pk>/', views.JewelryDetailView.as_view(), name='jewelryPiece'),
    path('articles/<int:objID>/', views.article, name='article'),
    path('jewelry/new/', login_required(views.JewelryCreateView.as_view()), name='newJewelry'),
    path('jewelry/<pk>/edit/', login_required(views.JewelryUpdateView.as_view()), name='editJewelry'),
    path('jewelry/<pk>/delete/', login_required(views.JewelryDeleteView.as_view()), name='deleteJewelry'),
    #re_path(r'^$',views.like_button, name='like'),
    path('like/', views.like_button, name='like'),
    path('tagged/<str:tag>/', views.Tagged.as_view(), name='tagged'),
    #path('tagged/', views.Tagged.as_view(), name='tagged'),
    path('user/<str:slug>/', views.ProfileDetailView.as_view(), name='profile'),
    #path('user/<str:slug>/edit/', login_required(views.ProfileUpdateView.as_view()), name='profileUpdate'),
    path('user/<str:slug>/edit/', login_required(views.profileUpdateView), name='profileUpdate'),
    path('file/<int:pk>/', views.downloadFile, name='downloadFile')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
