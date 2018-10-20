import json
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from . import models, github

def get_all_users():
    return [c.username for c in models.Contestant.objects.all()]

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
    models.Contestant.objects.get(username=username)
    return JsonResponse(g.get_user(username).raw_data)


@cache_page(60)
def event_info(request, event_id):
    event = models.Event.objects.get(id=event_id)
    return JsonResponse({
        username: github.get_user_activity(username, event.start, event.end)
        for username in get_all_users()
    })

@cache_page(60)
def event_info2(request, event_id):
    event = models.Event.objects.get(id=event_id)
    return JsonResponse(json.loads(event.cache))
