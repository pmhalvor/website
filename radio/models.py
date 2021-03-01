from django.db import models


class Suggest(models.Model):
    artists  = models.CharField('artists', max_length=200)
    sub_date = models.CharField('sub_date', max_length=200)
    track_id = models.CharField('track_id', max_length=200)
    track    = models.CharField('track', max_length=200)

    def __str__(self):
        return self.track

class History(models.Model):
    track_id  = models.CharField('track_id', max_length=23)
    played_at = models.DateTimeField('played_at')
    artist    = models.CharField('artist', max_length=150)
    track     = models.CharField('track', max_length=150)
    
    def __str__(self):
        return self.artist + ' - ' + self.track 