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

class Update(models.Model):
    title = models.CharField('title', max_length=50)
    descr = models.CharField('description', max_length=200)
    file_loc = models.URLField('url', max_length=200)
    img_loc  = models.ImageField(upload_to='img/', default='img/lookingcolors.jpg')
    pub_date = models.DateTimeField('pub_date')

    def __str__(self):
        return self.title

class Notes(models.Model):
    title = models.CharField('title', max_length=50)
    descr = models.CharField('description', max_length=200)
    file_loc = models.FileField(upload_to='notes/')
    img_loc  = models.ImageField(upload_to='img/', default='img/lookingcolors.jpg')
    pub_date = models.DateTimeField('pub_date')

    def __str__(self):
        return self.title


class Code(models.Model):
    title = models.CharField('title', max_length=50)
    descr = models.CharField('description', max_length=200)
    url = models.URLField('url', max_length=200)
    img_loc  = models.ImageField(upload_to='img/', default='img/lookingcolors.jpg')
    pub_date = models.DateTimeField('pub_date')

    def __str__(self):
        return self.title +' '+ self.url
