from django.urls import path
from . import views

app_name='home'
urlpatterns=[
    #.com/home/
    path('', views.index, name='index'),
    #.com/home/about
    path('about/', views.about, name='about'),
    #.com/home/codes/
    path('code/', views.code, name='code'),
    #.com/home/cv
    path('cv/', views.cv, name='cv'),
    #.com/home/notes
    path('notes/', views.notes, name='notes'),
    #.com/home/visuals
    path('visuals', views.visuals, name='visuals'),
]