from django.contrib import admin
from django.urls import path, include, re_path
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/',
        RegistrationView.as_view(success_url='/'),
        name='django_registration_register'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'), 
    re_path(r'^login/$', LoginView.as_view(), {"next_page": '/'}),
]