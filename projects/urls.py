from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django_registration.backends.one_step.views import RegistrationView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/',
        RegistrationView.as_view(success_url='/home'),
        name='django_registration_register'),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'), 
    re_path(r'^login/$', LoginView.as_view(), {"next_page": '/'}),

    path('home/', views.home, name='home'),
    re_path(r'^search/$', views.search, name='search'),
    path('newProject/', views.newProject, name='newProject'),
    # path('profile/', views.updateProfile, name='profile'),

    re_path(r'^api/profile/$', views.ProfileList.as_view())
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)