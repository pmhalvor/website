# Generated by Django 3.1.4 on 2020-12-14 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cv',
            old_name='location',
            new_name='loc',
        ),
        migrations.RenameField(
            model_name='cv',
            old_name='main_title',
            new_name='main',
        ),
        migrations.RenameField(
            model_name='cv',
            old_name='start_time',
            new_name='start',
        ),
        migrations.RenameField(
            model_name='cv',
            old_name='stop_time',
            new_name='stop',
        ),
        migrations.RenameField(
            model_name='cv',
            old_name='sub_title',
            new_name='sub',
        ),
        migrations.AddField(
            model_name='cv',
            name='cat',
            field=models.CharField(default='Work', max_length=200, verbose_name='category'),
            preserve_default=False,
        ),
    ]