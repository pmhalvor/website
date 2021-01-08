from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.radio, name='radio'),
    path('current/', views.Http_current, name='current'),
    path('recents/', views.Http_recents, name='recents'),
]