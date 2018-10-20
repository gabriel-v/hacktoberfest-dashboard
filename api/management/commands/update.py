from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from api import models
from api import github
import json
import time

class Command(BaseCommand):
    help = 'Query GitHub for new PR data'

    def add_arguments(self, parser):
        parser.add_argument('refresh', type=int, default=55)

    def handle(self, *args, **options):
        refresh_interval = options['refresh']
        while True:
            now = time.time()
            github.update_all()
            elapsed = time.time() - now
            remaining = max(10, refresh_interval - elapsed)
            time.sleep(remaining)
