from datetime import datetime, timedelta

def parse_recents(data = None) -> list:
    content = []
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


def parse_current(data = None) -> dict:
    content = {}

    # TODO

    return content
