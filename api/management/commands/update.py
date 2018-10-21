from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from api import models
from api import github
import json
import time

PERIOD = 2 * 60
MIN_WAIT = 20

class Command(BaseCommand):
    help = 'Query GitHub for new PR data'

    def handle(self, *args, **options):
        while True:
            now = time.time()
            print("---------------------------")
            github.update_all()
            elapsed = time.time() - now
            remaining = max(MIN_WAIT, PERIOD - elapsed)
            time.sleep(remaining)
