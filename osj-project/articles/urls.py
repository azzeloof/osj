from django.urls import path
from . import views

urlpatterns = [
    path('', views.allArticles, name='articles'),
    path('<int:objID>/', views.article, name='article')
]
