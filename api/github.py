import pytz
import json
import string
import requests

from django.conf import settings
from dateutil.parser import parse as parse_date
from . import models

from github import Github
rest = Github(settings.GITHUB_TOKEN)

GITHUB_API = 'https://api.github.com/graphql'

def get_pull_requests(username):
    def get(username, after):
        query = '''\
            query ($login:String!, $first:Int!, $after:String,$before:String) {
              user(login:$login) {
                pullRequests(first:$first,after:$after,before:$before) {
                  nodes{
                    repository {
                      nameWithOwner
                    }
                    number
                    createdAt
                  }
                  pageInfo {
                    endCursor
                  }
                }
              }
            }
        '''

        variables = {
            'login':username,
            'first': 99,
            'after': after,
        }

        resp = requests.post(
            GITHUB_API,
            json={'query': query, 'variables': variables},
            auth=('Bearer', settings.GITHUB_TOKEN),
        )
        return resp.json()['data']

    after = None
    while True:
        r = get(username, after)
        #import pdb; pdb.set_trace()
        after = r.get('user', {}).get('pullRequests', {}).get('pageInfo', {}).get('endCursor')
        prs = r.get('user', {}).get('pullRequests', {}).get('nodes', [])
        for pr in prs:
            yield pr
        if not after:
            break

def update_all():
    events = {}
    for user in [c.username for c in models.Contestant.objects.all()]:
        pull_requests = list(get_pull_requests(user))
        print("user", user, "has", len(pull_requests), "pull requests in total")
        for event in models.Event.objects.all():
            user_is_new = True
            relevant = []
            for pr in pull_requests:
                created = parse_date(pr['createdAt'])
                if created < event.start:
                    user_is_new = False
                if created < event.end and created > event.start:
                    relevant.append(pr)
            user_entry = events.setdefault(event.id, {}).setdefault(user, {})
            user_entry['inactive_before_event'] = user_is_new
            user_entry['pull_requests'] = [rest.get_repo(r['repository']['nameWithOwner']).get_pull(r['number']).raw_data for r in relevant]

    for event in models.Event.objects.all():
        event.cache = json.dumps(events[event.id])
        event.save()


def get_user_activity(username, start, end):
    user = rest.get_user(username)
    pull_requests = []
    for event in user.get_public_events():
        event_created = pytz.timezone("UTC").localize(event.created_at, is_dst=None)
        if event_created > end:
            continue
        if event_created < start:
            break
        if event.type != 'PullRequestEvent' or not event.public:
            continue
        if event.payload['action'] != 'opened':
            continue

        repo = event.repo.name
        number = event.payload['number']
        pull_request = rest.get_repo(repo).get_pull(number)
        pull_requests.append(pull_request.raw_data)

    return {
        "pull_requests": pull_requests,
    }
