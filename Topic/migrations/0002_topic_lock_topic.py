# Generated by Django 2.2.17 on 2020-12-01 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Topic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='lock_topic',
            field=models.BooleanField(default=False, verbose_name='Lock'),
        ),
    ]
