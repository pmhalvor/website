from django.db import models


class Suggest(models.Model):
    artists  = models.CharField('artists', max_length=200)
    sub_date = models.CharField('sub_date', max_length=200)
    track_id = models.CharField('track_id', max_length=200)
    track    = models.CharField('track', max_length=200)

    def __str__(self):
        return self.track
    