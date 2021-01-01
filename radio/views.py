from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .worker.song_history import get_recents
from .worker.authorize import get_token


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
			played_at = song['played_at']
			name = song['track']['name'].replace(',','')
			song_id = song['track']['id']
			artist = song['track']['artists'][0]['name'].replace(',','')

			content.append({'artist':artist, 'name':name, 'played_at':played_at})

	return content

