"""osj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from osj import views as core_views
from osj.forms import UserLoginForm
import notifications.urls

urlpatterns = [
    path('', include('pages.urls'), name='index'),
    path('admin/', admin.site.urls),
    path(
        'auth/login/',
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
            ),
        name='login'
        ),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/register', core_views.registration, name='registration'),
    path('auth/whatsnext', core_views.afterRegistration, name='afterRegistration'),
    path('tinymce/', include('tinymce.urls'), name='tinymce'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('tz_detect/', include('tz_detect.urls')),
    re_path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
