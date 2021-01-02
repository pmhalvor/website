from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .worker.song_history import get_recents
from .worker.authorize import get_token
from datetime import datetime, timedelta



def index(request):
	return HttpResponse("Welcome to Per's cool Radio!")

def radio(request):
	context = {}
	context['recents'] = recents()
	return render(request, 'radio/index.html', context=context)


def recents():
	token = get_token()
	data = get_recents(token)['items']
	content = []

	if data:
		for song in data[:20]:
			played_at = str(datetime.strptime(song['played_at'],  '%Y-%m-%dT%H:%M:%S.%fZ')
							+ timedelta(hours=1))[:-3]
			name = song['track']['name'].replace(',','')
			song_id = song['track']['id']
			artist = song['track']['artists'][0]['name'].replace(',','')

			content.append({'artist':artist, 'name':name, 'played_at':played_at})

	return content

