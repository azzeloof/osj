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
    path('file/<int:pk>/', views.downloadFile, name='downloadFile'),
    path('notifications', views.notifications, name="notifications"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
