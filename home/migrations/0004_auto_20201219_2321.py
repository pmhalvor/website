# Generated by Django 3.1.4 on 2020-12-19 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='update',
            name='upload',
        ),
        migrations.AddField(
            model_name='update',
            name='_file',
            field=models.FileField(default='notes/SpotifyVisuals.html', upload_to='notes/'),
        ),
        migrations.AddField(
            model_name='update',
            name='_img',
            field=models.ImageField(default='img/lookingcolors.jpg', upload_to='img/'),
        ),
    ]