from django.urls import path
from . import views

app_name='home'
urlpatterns=[
    #.com/home/
    path('', views.UpdateView.as_view(), name='index'),
    #.com/home/about
    path('about/', views.about, name='about'),
    #.com/home/codes/
    path('code/', views.CodeView.as_view(), name='code'),
    #.com/home/cv
    path('cv/', views.CvView.as_view(), name='cv'),
    #.com/home/notes
    path('notes/', views.NotesView.as_view(), name='notes'),
    #.com/home/visuals
    path('prompts/', views.prompts, name='prompts'),
]
