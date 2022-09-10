from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from datetime import datetime, timedelta

import json
import plotly.graph_objs as go
import plotly.offline as opy

# from radio.models import History
from .worker.authorize import get_token
from .worker.plot import artist_duration, song_plays
from .worker.parse import parse_recents, parse_current
from .worker.song_history import get_recents, get_current

def index(request):
	return HttpResponse("Welcome to Per's Radio!")

def radio(request):
	# should just be all the "other content" on the page
	context = {}
	context['welcome'] = "" #"Welcome to the site radio."
	context['intro'] =  """ """
	# Here you can see what I'm currently listening to, 
	# and some of the recents songs I've heard.
	# This web-app is still in development, 
	# so check back in later for even more cool features.
	# """

	return render(request, 'radio/index.html', context)


def current(request):
	# spotify token for new api calls
	token = get_token()

	# current listen activity
	data = get_current(token)

	#parse response for jinja
	context = {'current':parse_current(data)}

	return render(request, 'includes/current.html', context)


def recents(request):
	# spotify token for new api calls
	token = get_token()

	# recently played
	data = get_recents(token)['items']

	# parse response for jinja
	context = {'recents' : parse_recents(data)} 

	return render(request, 'includes/recents.html', context)


def plots(request):
	context = {}
	context['plot_artists'] = artist_duration() #(History)
	context['plot_songs'] = song_plays() #(History)
	return render(request, 'includes/plots.html', context)


def update(request, section='current'):
	if section == 'current':
		# spotify token for new api calls
		token = get_token()

		data = get_current(token)

	try:
		# parse response for jinja
		context = {section:parse_current(data)}


	except Exception as e:
		context = {'error':str(e), 'failed':True, 'section': section, 'data':data}

	# return json.dumps(context)
	return HttpResponse(json.dumps(context), content_type="application/json")
