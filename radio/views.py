from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from datetime import datetime, timedelta

import json
import plotly.graph_objs as go
import plotly.offline as opy

from radio.models import History
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


### LOAD PAGE
def old_current():
	"""
	Return the template for div.playing
	"""
	content = {}

	# spotify token for new api calls
	token = get_token()

	# recently played
	data = get_current(token)

	# if data:
	try:
		url 	 = data['item']['external_urls']['spotify']
		artwork  = data['item']['album']['images'][0]['url']
		track 	 = data['item']['name']
		artist 	 = data['item']['artists'][0]['name']
		duration = data['item']['duration_ms']
		progress = data['progress_ms'] #round(data['progress_ms']/duration*100, ndigits=1)
	except:
		# else:
		url	 = 'https://www.spotify.com' 
		artwork  = 'https://perhalvorsen.com/media/img/empty_album.png'
		track    = 'nothing playing'
		artist   = ''
		duration = 0 
		progress = 0

	content['url'] 	= url
	content['artwork'] 	= artwork
	content['track'] 	= track
	content['artist'] 	= artist
	content['duration'] = duration
	content['progress'] = progress

	return content

def old_recents():
	content = []

	# spotify token for new api calls
	token = get_token()

	# recently played
	data = get_recents(token)['items']

	# extracting specific details
	if data:
		for song in data[:20]:
			track_url = song['track']['external_urls']['spotify']
			try:
				played_at = str(datetime.strptime(song['played_at'],  '%Y-%m-%dT%H:%M:%S.%fZ')
							+ timedelta(hours=1))[:-3]
			except:
				played_at = str(datetime.strptime(song['played_at'],  '%Y-%m-%dT%H:%M:%SZ')
							+ timedelta(hours=1))[:-3]
			name = song['track']['name'].replace(',','')
			song_id = song['track']['id']
			artist = song['track']['artists'][0]['name'].replace(',','')
			artist_url = song['track']['artists'][0]['external_urls']['spotify']

			content.append({'artist':artist, 'artist_url':artist_url, 
							'name':name, 'played_at':played_at, 
							'track_url': track_url})

	return content

def Http_current(request):
	# needs to be json to get progress and duration varaibles
	return HttpResponse(json.dumps(old_current()), content_type="application/json")

def Http_recents(request):
	return render(None, 'includes/recents.html', {'recents': old_recents()})


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
	context['plot_artists'] = artist_duration(History)
	context['plot_songs'] = song_plays(History)
	return render(request, 'includes/plots.html', context)


def update(request, section='current'):
	# TODO refactor this away using jinja better
	if section == "recents":
		return recents(request)
	# spotify token for new api calls
	token = get_token()

	data = None
	try:
		# hacky call local function 
		data = globals()[f'get_{section}'](token)
	
		# data = data['items'] if section=='recents' else data
		
		# parse response for jinja
		context = {section:globals()[f'parse_{section}'](data)}


	except Exception as e:
		context = {'error':str(e), 'failed':True, 'section': section, 'data':data}

	# return json.dumps(context)
	return HttpResponse(json.dumps(context), content_type="application/json")
