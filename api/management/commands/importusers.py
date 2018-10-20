from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from api import models
import json

class Command(BaseCommand):
    help = 'Adds users to list'

    def add_arguments(self, parser):
        parser.add_argument('json_list_file', type=str)

    def handle(self, *args, **options):
        with open(options['json_list_file'], 'r') as f:
            users = json.load(f)
            for user in users:
                if models.Contestant.objects.filter(username=user).exists():
                    print("Skipped", user, "- already added")
                    continue
                try:
                    models.Contestant(username=user).save()
                    print("Added", user)
                except IntegrityError as e:
                    print("Error adding", user, "- not found")
