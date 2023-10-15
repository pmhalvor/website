# perhalvorsen.com (master)

Hello and welcome to my site!

This master branch represents the latest, stable version of the site.
Checkout the development branch to see what I currently am working on. 
Otherwise, take a peek at the previous releases of the site, to see what
 changes have been implemented.


Changelog:
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


I use this site as a portfolio, shining light on some of the web-development 
projects I've taken part in.
If there are any malfunctions on your end, 
send me an email or pull request, and I'll work on
fixing it.


# Useful commands when developing

### Add entry to database

First, nagivate to the folder, activate the environment, and open a python shell in the project:
```sh
cd /path/to/site
source siteenv/bin/activate
python manage.py shell
```

Then, import the model you want to add new entry for, along with the interactive-adder tool.
Models and their fields can be found at [home/model.py](home/models.py).

```python
from home.models import Notes
from tools.table import interactive_add, to_dt

interactive_add(Notes)

>>> title: My New Note
>>> descr: Small description of content
>>> file_loc: path/to/this/note.md
>>> img_loc: path/to/note/image.png
>>> pub_date: to_dt(year=2023, month=7, day=3)
>>> Added: {...}
``` 


### Restart server 

if you make any changes to `settings.py` or other places in the project that aren't showing up right away,
 you may need to restart the server. This is easily done with:
```sh
source restart.sh
```
