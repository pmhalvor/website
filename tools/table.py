from home.models import *
from django.utils import timezone

def get_columns(model):
    return [f.name for f in model._meta.get_fields()]

def interactive_add(model):
    add_dict = {}

    for column in get_columns(model):
        if column=='id':
            continue
        value = input(column+': ')

        # allows for calling functions in input
        if value[0] == '_':
            exec('v = '+value[1:], globals())
            value = globals()['v']

        add_dict[column] = value
    
    new = model(**add_dict) # add new instance with this data
    new.save()

    return print('Added: ', add_dict)

def to_dt(year=None, month=None, day=None):
    now = timezone.now()
    if year:
        now = now.replace(year=year)
    if month:
        now = now.replace(month=month)
    if day:
        now = now.replace(day=day)
    return now