from radio.models import Suggest
from tools.table import to_dt
from django.http import HttpResponse, HttpRequest
import json
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def submit_suggestions(request):
    items = request.POST.getlist('items')
    # artists = request.POST.getlist('artists')
    # track = request.POST.get('track')
    # track_id = request.POST.get('id')
    return HttpResponse(len(items))

# if request.POST.get('item'):
# else:
#     return HttpResponse("did not work")
# data = json.loads(str(request.GET))
# # data = request.POST.get('item')
# # artists = data.get('artists')
# # artists = request.POST['artists']
# # track = request.POST['track']
# # track_id = request.GET['id']
# # sub_date= to_dt()
# # artists = request.POST['artists']
# # track = request.POST['track']
# # track_id = request.GET['id']
# # sub_date= to_dt()

# # new = Update(artist=artist, sub_date=sub_date, track=track, track_id=track_id)
# # new.save()

# return HttpResponse("{'msg': 'success', 'datatype':"+str(data)+"}", content_type="application/json")
	