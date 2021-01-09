from radio.models import Suggest
from tools.table import to_dt


def submit_suggestions(request):
    data = request.GET.get('data')
    artist = data.get('artist')
    track = data.get('track')
    track_id = data.get('track_id')
    sub_date= to_dt()

    new = Update(artist=artist, sub_date=sub_date, track=track, track_id=track_id)
    new.save()

    return 'Success'
	