from django.contrib import admin
from django.urls import include, path
from . import views
from .worker import search, submit, plot

urlpatterns = [
    path('', views.radio, name='radio'),
    path('current/', views.current, name='current'),
    path('plots/',   views.plots , name='plots'),
    path('recents/', views.recents, name='recents'),
    path('update/<str:section>', views.update, name='update'),
    path('search/', search.Http_search, name='search'),
    path('submit/', submit.submit_suggestions , name='submit'),
]
