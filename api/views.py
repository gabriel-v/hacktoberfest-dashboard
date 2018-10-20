import pytz
import string
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from . import models

GITHUB_API = 'https://api.github.com/graphql'


@cache_page(60)
def data(request):
    query = '''\
        query ($login:String!, $first:Int!, $after:String,$before:String) {
          viewer {
            login
            name
          }
          codesOfConduct {
            name
          }
          user(login:$login) {
            pullRequests(first:$first,after:$after,before:$before) {
              nodes{
                repository {
                  nameWithOwner
                }
                number
              }
              pageInfo {
                endCursor
              }
            }
          }
        }
    '''

    variables = {
        'login': models.Contestant.objects.first().username,
        'first': 100,
        'after': None,
    }

    resp = requests.post(
        GITHUB_API,
        json={'query': query, 'variables': variables},
        auth=('Bearer', settings.GITHUB_TOKEN),
    )

    return JsonResponse(resp.json())
