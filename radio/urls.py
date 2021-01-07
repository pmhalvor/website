from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.radio, name='radio'),
    # path('', views.current, name='current'),
]