"""Defines URL patterns for users"""

from django.conf.urls import url
from django.contrib.auth.views import LoginView
from . import views


app_name = 'users'

urlpatterns = [
    # login page
    url(r'^ login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    #  logout page
    url(r'^logout/$', views.logout_view, name='logout'),
    # registration page
    url(r'^register/$', views.register, name='register'),
]