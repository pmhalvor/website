from django.utils import timezone
import json

def get_columns(model):
    return [f.name for f in model._meta.get_fields()]

def safe_add(model):
    try:
        interactive_add(model)
    except Exception as e:
        print(e)

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

def dict_add(model, dic):
    new = model(**dic) # add new instance with this data
    new.save()

    return print('Added: ', add_dict)

def add_df(model, df, columns={}):
    '''
    Add dataframe to database
    Params:
        columns: user defined column mapping from df to db
            defaulf=columns from db
    '''
    # rename columns according to specified mapping
    if columns:
        df = df.rename(columns=columns)

    # for entries that throw error
    errors = []

    # translate to a dict of dicts, by index
    data = json.loads(df.to_json(orient='index'))
    for i in data.keys():
        try:
            # all entries should be new, but just in case
            obj, created = model.objects.get_or_create(**data[i])
            if created:
                print(f'Entry {data[i]} added')
            else:
                print(f'Entry {data[i]} already exists in db')
        except:
            errors.append(str(data[i]))

    print('finished adding new entries')
        
    return errors

def to_dt(year=None, month=None, day=None):
    now = timezone.now()
    if year:
        now = now.replace(year=year)
    if month:
        now = now.replace(month=month)
    if day:
        now = now.replace(day=day)
    return now
