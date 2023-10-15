"""
WSGI config for phsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
import json
import os

from django.core.wsgi import get_wsgi_application

# load env vars from local json via absolute path
with open("/home/pmhalvor/site/phsite/config.json") as f:
    config = json.load(f)

# check required keys are actually present in config.json
for required_key in ['AZURE_STORAGE', 'DJANGO_SECRET', 'POSTGRES_PASSWORD', 'ROOT', 'SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET']:
    assert required_key in config.keys()

# force feed environment vars, fail if var not in config.json 
for key, value in config.items():
    os.environ.setdefault(key, value)

# added in tutorial
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phsite.settings')


application = get_wsgi_application()
