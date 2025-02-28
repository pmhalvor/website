from django.shortcuts import render
from django.views import generic
from django.views.decorators.cache import never_cache
from home.models import Cv, Update, Notes, Code
from django.utils import timezone
from django import template
from datetime import timedelta
from django.shortcuts import redirect
from .prompts_data import prompts_list  # Import the list

register = template.Library()

class CvView(generic.ListView):
    template_name = 'home/cv.html'
    model = Cv 


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cv_list'] = Cv.objects.all()
        context['work_list'] = Cv.objects.filter(cat='Work').order_by('-start')
        context['edu_list'] = Cv.objects.filter(cat='Education')
        context['lang_list'] = self.get_lang_list_correct_time()
        context['now'] = timezone.now().astimezone(timezone.get_current_timezone())

        return context

    def get_lang_list_correct_time(self):
        lang_list = []
        now = timezone.now().astimezone(timezone.get_current_timezone())
        for item in Cv.objects.filter(cat='Language').order_by('start'):
            if item.start.month > now.month:
                year = item.start.year + 1
                month = 12 - abs(now.month - item.start.month)
                kwargs = {'year':year, 'month':month}
                item.start = item.start.replace(**kwargs)

            lang_list.append(item)
        return lang_list


class UpdateView(generic.ListView):
    template_name = 'home/index.html'
    model = Update

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_list'] = Update.objects.all().order_by('-pub_date')[:7] # most recent 7
        return context


class NotesView(generic.ListView):
    template_name = 'home/notes.html'
    model = Notes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes_list'] = Notes.objects.all().order_by('-pub_date')
        return context


class CodeView(generic.ListView):
    template_name = 'home/code.html'
    model = Code

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['code_list'] = Code.objects.all().order_by('-pub_date')
        return context


def about(request):
    return render(request, 'home/about.html')

def code(request):
    return render(request, 'home/code.html')

def notes(request):
    return render(request, 'home/notes.html')

@never_cache
def prompts(request):
    context = {'prompts_list': prompts_list}  # Pass the list in the context
    return render(request, 'home/prompts.html', context)
