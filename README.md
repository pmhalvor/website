# perhalvorsen.com 
Repository for my personal website, [perhalvorsen.com](https://perhalvorsen.com).

This master branch represents the latest, stable version of the site.
Checkout the development branch to see what I currently am working on. 
Otherwise, take a peek at the previous releases of the site, to see what
 changes have been implemented.



I use this site as a portfolio, shining light on some of the web-development 
projects I've taken part in.
If there are any malfunctions on your end, 
send me an email or pull request, and I'll work on
fixing it.

## Changelog:
- 2.1.0: Updated server to Ubuntu 4.23 and ensure environment vars present
- 2.0.0: Migrated off of Azure. Everything is now soley hosted on Digial Ocean server
- 1.1.4: current, recents, and plots loaded seperately from `/radio`, allowing for smoother user experience
- 1.1.3: Radio branch now serving data locally for fewer server timeouts on page refresh
- 1.1.2: Radio branch now has plots showing data from Azure storage
- 1.1.1: Radio branch incorperating calls to the [Spotify API](developers.spotify.com)
- 1.0.5: Code stored in database on server. Items served dynamically using Django.
- 1.0.4: Notes stored in database on server. Page items are pulled dynamically using Django.
- 1.0.3: Home page updates stored in database on server. Items pulled dynamically from Django.
- 1.0.2: Cv entries stored in database. Served dynamically using Django.
- 1.0.1: Static site from previous deploy hosted from server.


# Useful commands when developing

## Run site container
Uses `docker compose` to build, run, then tear down the site container. 
```sh
make run
```


## Restart server 

if you make any changes to `settings.py` or other places in the project that aren't showing up right away (i.e. radio plots, css formatting, html templates),
 you may need to restart the server. This is easily done with:
```sh
source restart.sh
```

## Changes to the database 
The database serves data to various pages on the site, from the CV items, to notes and updates. 
You can add changes through the Django GUI at https://perhalvorsen.com/admin, or via command line. 
These next few tips will show how to execute these changes through a Python shell in the command line. 

First, nagivate to the folder, activate the environment, and open a python shell in the project:
```sh
cd /path/to/site
source siteenv/bin/activate
python manage.py shell
```

### Add entry to database

To add a new entry, import the model you want to add the entry for, along with the interactive-adder tool.
Models and their fields can be found at [home/model.py](home/models.py).

```python
from home.models import Notes
from tools.table import interactive_add, to_dt

interactive_add(Notes)

>>> title: My New Note
>>> descr: Small description of content
>>> file_loc: /path/to/this/note.md
>>> img_loc: path/to/note/image.png
>>> pub_date: 2023-07-03
>>> Added: {...}
``` 

### Update entry in database
To update an item currently present in the database, you'll again need to import the desired model.
You will also need to know the unique field identifier for that item, usually `title` or `main`.

Building off the previous exmaple, we would get something like:
```python
from home.models import Notes

new_note = Notes.objects.get(title="My New Note")

print(new_note.file_loc)
new_note.file_loc = "/new/path/to/note.md"
print(new_note.file_loc)

new_note.save()

>>> '/path/to/this/note.md'
>>> '/new/path/to/note.md'
```


If you want to see all the items listed for that model, run `Notes.objects.get_queryset()`. 

