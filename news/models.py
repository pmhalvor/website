from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class Post(models.Model):
    post_title = models.CharField('title', max_length=100)
    pub_date = models.DateTimeField('date published')
    post_html = models.CharField('file', max_length=1000000)
    def __str__(self):
        return self.post_title


class CV(models.Model):
    