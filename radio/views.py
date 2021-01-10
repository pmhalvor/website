from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .worker.song_history import get_recents, get_current
from .worker.authorize import get_token
from datetime import datetime, timedelta
import json



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
	context['recents'] = recents()
	context['current'] = current()
	return render(request, 'radio/index.html', context)


### LOAD PAGE
def current():
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
		url		 = 'https://www.spotify.com' 
		artwork  = 'https://perhalvorsen.com/media/img/empty_album.png'
		track    = 'nothing playing'
		artist   = ''
		duration = 0 
		progress = 0

	content['url'] 		= url
	content['artwork'] 	= artwork
	content['track'] 	= track
	content['artist'] 	= artist
	content['duration'] = duration
	content['progress'] = progress

	return content

def recents():
	content = []

	# spotify token for new api calls
	token = get_token()

	# recently played
	data = get_recents(token)['items']

	# extracting specific details
	if data:
		for song in data[:20]:
			track_url = song['track']['external_urls']['spotify']
			played_at = str(datetime.strptime(song['played_at'],  '%Y-%m-%dT%H:%M:%S.%fZ')
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
	return HttpResponse(json.dumps(current()), content_type="application/json")

def Http_recents(request):
	return render(None, 'includes/recents.html', {'recents': recents()})
