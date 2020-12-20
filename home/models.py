from django.db import models
# from .storage import ExistingFileStorage

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

### need to make it so that updates with same file name replace the previous versions.
### need to figure out how to properly link to these files/images
### maybe try selecting from already in database?
###     would point is to show updaets....?
### point to absolute links?
###     but media/fiels is not available..?


# efs = ExistingFileStorage()
class Update(models.Model):
    title = models.CharField('title', max_length=200)
    descr = models.CharField('description', max_length=200)
    file_loc = models.FileField(upload_to='files/', default='files/SpotifyVisuals.html')
    img_loc  = models.ImageField(upload_to='img/', default='img/lookingcolors.jpg')
    pub_date = models.DateTimeField('pub_date')

    def __str__(self):
        return self.title