from django.shortcuts import render
from django.views import generic
from home.models import Cv
from django.utils import timezone

class CvView(generic.ListView):
    template_name = 'home/cv_empty.html'
    model = Cv 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cv_list'] = Cv.objects.all()
        context['work_list'] = Cv.objects.filter(cat='Work')
        context['edu_list'] = Cv.objects.filter(cat='Education')
        context['lang_list'] = Cv.objects.filter(cat='Language').order_by('start')
        context['now'] = timezone.now()

        return context


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
