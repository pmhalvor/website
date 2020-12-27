from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('', views.RadioView.as_view(), name='radio'),
    path('', views.radio, name='radio'),
]