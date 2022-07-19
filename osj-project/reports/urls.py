from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('new/<str:model>/<int:pk>', login_required(views.NewReport.as_view()), name='new_report'),
]
