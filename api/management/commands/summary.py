from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from api import models
from api import github
import json
import time

class Command(BaseCommand):
    help = 'Print details about each event'

    def add_arguments(self, parser):
        parser.add_argument('event_id', type=int)

    def handle(self, *args, **options):
        event_id = options['event_id']
        event = models.Event.objects.get(id=event_id)
        data = json.loads(event.cache)
        total = 0
        have_prs = []
        newcomers = []
        for user in data:
            userdata = data[user]
            total += len(userdata['pull_requests'])
            print(user, userdata['inactive_before_event'], len(userdata['pull_requests']))
            if userdata['inactive_before_event']:
                newcomers.append(user)
            if len(userdata['pull_requests']):
                have_prs.append(user)
        print('total: ', total, 'prs')
        print('newcomers: ', len(newcomers), newcomers)
        print('have prs: ', len(have_prs), have_prs)
