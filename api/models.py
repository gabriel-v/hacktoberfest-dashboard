from django.db import models, IntegrityError
from .github import rest

class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    name = models.CharField(max_length=200)
    cache = models.TextField(blank=True)


class Contestant(models.Model):
    username = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        try:
            u = rest.get_user(self.username)
        except Exception as e:
            raise IntegrityError('github username not found: ' + self.username)
        models.Model.save(self, *args, **kwargs)
