from django.http import HttpResponse
from django.shortcuts import render
import uuid
from .models import StateCode, RedditUser
from .reddit_auth import get_auth_url, get_refresh_token, get_reddit_instance


def auth_thanks(request):
    query_terms = request.GET.copy()
    code = query_terms['code']

    refresh_token = get_refresh_token(code)
    user_obj = RedditUser.objects.create(refresh_token=refresh_token)
    username = get_reddit_instance(user_obj).user.me().name

    if StateCode.exists(query_terms['state']):
        return render(request, 'deleteme_bot/auth_thanks.html', {'username': username})
    else:
        return HttpResponse('Something has gone wrong - we were not expecting that state code')


def landing(request):
    state_code = uuid.uuid4().hex
    auth_url = get_auth_url(state_code=state_code)
    StateCode.objects.create(state_code=state_code)

    return render(request, 'deleteme_bot/landing.html', {'auth_url': auth_url})
