from os import stat
from django.db import models
from django.db.models.fields import SlugField
from django.utils import timezone

import requests 
from requests.utils import quote #percent encoding
import os
import datetime
from datetime import datetime, timedelta


# Create your models here.

class Broadcaster(models.Model):
    broadcaster_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Clip(models.Model):
    slug = SlugField(primary_key=True)
    title = models.CharField(max_length=300)
    views = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    twitch_url = models.URLField(max_length=300) #twitch url
    local_url = models.URLField(max_length=300) #local url
    author = models.CharField(max_length=100)
    duration = models.DurationField()
    broadcaster = models.ForeignKey(Broadcaster, models.SET_NULL, null=True)
    game = models.ForeignKey(Game,  on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.title, self.broadcaster, self.timestamp)
