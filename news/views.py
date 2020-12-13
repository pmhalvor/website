from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
#from news.models import Post
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


#class IndexView(generic.ListView):
#    template_name = ''

def index(request):
    f = open('../static/pages/index.html')
    lines = f.read()
    f.close()
    return HttpResponse(lines)
