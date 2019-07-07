from django.contrib import admin
from .models import Profile, Song, SongPart, InstrumentPart, Group

admin.site.register(Profile)
admin.site.register(Song)
admin.site.register(SongPart)
admin.site.register(InstrumentPart)
admin.site.register(Group)
