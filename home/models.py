from django.db import models

# Create your models here.

class Cv(models.Model):
    main = models.CharField('main', max_length=200)
    sub  = models.CharField('sub', max_length=200)
    loc   = models.CharField('location', max_length=200)
    start = models.DateTimeField('start')
    stop  = models.DateTimeField('stop')
    cat = models.CharField('category', max_length=200)

    def __str__(self):
        return self.main