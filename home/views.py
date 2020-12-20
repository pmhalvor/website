from django.shortcuts import render
from django.views import generic
from home.models import Cv, Update
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

# class UpdateView(generic.ListView):
#     template_name = 'home/index_empty.html'
#     model = Update

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['update_list'] = Update.objects.all().order_by('pub_date')
#         return context

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













# class IndexView(generic.ListView):
#     template_name = 'old_site/index.html'
#     context_object_name = 'latest_question_list'

#     def get_queryset(self):
#         """Return the last fine puclished questions."""
#         return Question.objects.filter(
#             pub_date__lte=timezone.now() # lte: less than equal
#         ).order_by('-pub_date')[:5]


# class AboutView(generic.DetailView):
#     model = About
#     template_name = 'old_site/about.html'

#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return About.objects.filter(pub_date__lte=timezone.now())  #less than equal to

# class CodeView(generic.DetailView):
#     model = Question
#     template_name = 'old_site/code.html'

#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now())


# class CvView(generic.DetailView):
#     model = Question
#     template_name = 'old_site/cv.html'

#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now())


# class NotesView(generic.DetailView):
#     model = Question
#     template_name = 'old_site/notes.html'

#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())  #less than equal to


# class VisualsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'

#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now())









#############################    GRAVEYARD     #########################################
# # keep as before for comparison
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         # Redisplay the question voting form.
#         return render(request, 'polls/detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

