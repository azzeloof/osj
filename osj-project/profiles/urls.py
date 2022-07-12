from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<str:slug>/', views.ProfileDetailView.as_view(), name='profile'),
    path('<str:slug>/edit/', login_required(views.profileUpdateView), name='profileUpdate'),
] 
