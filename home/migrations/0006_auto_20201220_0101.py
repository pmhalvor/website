# Generated by Django 3.1.4 on 2020-12-20 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20201220_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='file_loc',
            field=models.FileField(default='files/SpotifyVisuals.html', upload_to='files/'),
        ),
    ]