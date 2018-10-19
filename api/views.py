import pytz
from django.http import JsonResponse
from django.conf import settings
from . import models

from django.views.decorators.cache import cache_page
from github import Github
g = Github(settings.GITHUB_TOKEN)


def get_all_users():
    return [c.username for c in models.Contestant.objects.all()]


def was_user_inactive_before(user, date):
    return False


def get_user_activity(username, start, end):
    user = g.get_user(username)
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
        pull_request = g.get_repo(repo).get_pull(number)
        pull_requests.append(pull_request.raw_data)

    return {
        "inactive_before_event": was_user_inactive_before(user, start),
        "pull_requests": pull_requests,
    }


def event_list(request):
    return JsonResponse({"events": [{
        "name": event.name,
        "start": event.start,
        "end": event.end,
        "id": event.id,
    } for event in models.Event.objects.all()]})


def user_list(request):
    return JsonResponse({"users": get_all_users()})


@cache_page(60)
def user_info(request, username):
    # Check that the username is registered.
    try:
        models.Contestant.objects.get(username=username)
    except models.Contestant.DoesNotExist:
        return JsonResponse({"error": "user not registered"}, status_code=404)

    return JsonResponse(g.get_user(username).raw_data)


@cache_page(60)
def event_info(request, event_id):
    try:
        event = models.Event.objects.get(id=event_id)
    except models.Event.DoesNotExist:
        return JsonResponse({"error": "event does not exist"}, status_code=404)

    return JsonResponse({
        username: get_user_activity(username, event.start, event.end)
        for username in get_all_users()
    })
