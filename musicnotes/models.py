from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Profile (one to one extension of User class)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preference = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.get_full_name())

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Group(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE)
    members = models.ManyToManyField(Profile, related_name="members")
    name = models.CharField(max_length=30)

    def __str__(self):
        return "Group " + str(self.name)


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    key = models.CharField(max_length=3)

    def __str__(self):
        return str(self.title) + " by " + str(self.artist)


class SongPart(models.Model):
    number = models.PositiveIntegerField()
    type_name = models.CharField(max_length=10, default='Verse')
    identifier = models.CharField(max_length=1, blank=True, default='')
    count = models.PositiveIntegerField(default=1)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.type_name) + " " + str(self.identifier)

class InstrumentPart(models.Model):
    instrument = models.CharField(max_length=30)
    song_part = models.ForeignKey(SongPart, on_delete=models.CASCADE)
    music = models.CharField(max_length=1000)
    capo = models.IntegerField()

    def __str__(self):
        return str(self.instrument) + " " + str(self.song_part)




