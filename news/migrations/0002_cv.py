# Generated by Django 3.1.4 on 2020-12-13 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintitle', models.CharField(max_length=200, verbose_name='main')),
                ('subtitle', models.CharField(max_length=200, verbose_name='sub')),
                ('title', models.CharField(max_length=200, verbose_name='main')),
            ],
        ),
    ]