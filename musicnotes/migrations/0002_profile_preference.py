# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2019-07-03 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicnotes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='preference',
            field=models.BooleanField(default=True),
        ),
    ]
