from django.db import models

class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.CharField(max_length=200)


class Contestant(models.Model):
    username = models.CharField(max_length=200)
