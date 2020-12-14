from django.db import models

# Create your models here.

class Cv(models.Model):
    main_title = models.CharField('main', max_length=200)
    sub_title  = models.CharField('sub', max_length=200)
    location   = models.CharField('location', max_length=200)
    start_time = models.DateTimeField('start')
    stop_time  = models.DateTimeField('stop')


    def __str__(self):
        return self.main_title