# Generated by Django 3.1.4 on 2021-01-09 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suggest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artists', models.CharField(max_length=200, verbose_name='artists')),
                ('sub_date', models.CharField(max_length=200, verbose_name='sub_date')),
                ('track_id', models.CharField(max_length=200, verbose_name='track_id')),
                ('track', models.CharField(max_length=200, verbose_name='track')),
            ],
        ),
    ]
