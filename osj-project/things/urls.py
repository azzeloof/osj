from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.JewelryListView.as_view(), name='jewelry'),
    path('<int:pk>/', views.JewelryDetailView.as_view(), name='jewelryPiece'),
    path('new/', login_required(views.JewelryCreateView.as_view()), name='newJewelry'),
    path('<pk>/edit/', login_required(views.JewelryUpdateView.as_view()), name='editJewelry'),
    path('<pk>/delete/', login_required(views.JewelryDeleteView.as_view()), name='deleteJewelry'),
    path('like/', views.like_button, name='like'),
    path('tagged/<str:tag>/', views.Tagged.as_view(), name='tagged'),
]