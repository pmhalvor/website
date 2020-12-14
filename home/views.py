from django.shortcuts import render
from django.views import generic
from home.models import Cv

# my code
# from django.http import HttpResponse, HttpResponseRedirect
# from django.utils import timezone
# from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from old_site.models import Index, About, Cv, Notes, Code, Visuals

class CvView(generic.ListView):
    template_name = 'home/cv_empty.html'
    context_object_name = 'cv_list'
    def get_queryset(self):
        return Cv.objects.all()



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

