from django.shortcuts import render
from django.views import generic
from django.utils import timezone


def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def code(request):
    return render(request, 'home/code.html')

def cv(request):
    return render(request, 'home/cv.html')

def notes(request):
    return render(request, 'home/notes.html')

def visuals(request):
    return render(request, 'home/visuals.html')
