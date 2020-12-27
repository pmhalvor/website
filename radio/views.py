from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

def index(request):
	return HttpResponse("Welcome to Per's cool Radio!")

def radio(request):
	context = {}
	context['response'] = other_func()
	return render(request, 'radio/index.html', context=context)


def other_func():
	to_return = ''
	for i in range(100):
		to_return += str(i**2/23)+' '
	return to_return

