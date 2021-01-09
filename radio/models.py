from django.db import models

# Create your models here.


class Suggest(models.Model):
    artist = models.CharField('artist', max_length=200)
    id = models.CharField('id', max_length=200)
    track = models.CharField('track', max_length=200)
    