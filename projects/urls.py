from django.contrib import admin
from django.urls import path, include
from django_registration.backends.one_step.views import RegistrationView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/',
        RegistrationView.as_view(success_url='/index/'),
        name='django_registration_register'),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]