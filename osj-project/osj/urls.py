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
from osj.forms import UserLoginForm, UserPasswordResetForm, UserPasswordChangeForm
import notifications.urls
from django_email_verification import urls as email_urls  # include the urls

urlpatterns = [
    path('', include('pages.urls'), name='index'),
    path('reports/', include('reports.urls'), name='reports'),
    path('admin/', admin.site.urls),
    path(
        'auth/login/',
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
            ),
        name='login'
        ),
    path(
        'auth/password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            form_class=UserPasswordResetForm
            ),
        ),
    path(
        'auth/password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
            form_class=UserPasswordChangeForm
            ),
        ),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/register', core_views.registration, name='registration'),
    path('auth/whatsnext', core_views.afterRegistration, name='afterRegistration'),
    path('tinymce/', include('tinymce.urls'), name='tinymce'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('tz_detect/', include('tz_detect.urls')),
    re_path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('email/', include(email_urls)),  # connect them to an arbitrary path
    path('newVerificationLink/', core_views.newVerificationLink, name='newVerificationLink')
]
