# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2019-07-03 12:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicnotes', '0002_profile_preference'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicnotes.Profile')),
                ('members', models.ManyToManyField(related_name='members', to='musicnotes.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instrument', models.CharField(max_length=30)),
                ('music', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=200)),
                ('key', models.CharField(max_length=3)),
                ('capo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SongPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
                ('type_name', models.CharField(default='Verse', max_length=10)),
                ('identifier', models.CharField(default='', max_length=1)),
                ('count', models.PositiveIntegerField(default=1)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='musicnotes.Song')),
            ],
        ),
        migrations.AddField(
            model_name='instrumentpart',
            name='song_part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='musicnotes.SongPart'),
        ),
    ]
