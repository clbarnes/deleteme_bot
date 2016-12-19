import os
from praw import Reddit
from django.urls import reverse

# todo
BASE_URL = 'http://localhost:8000'  # to allow redirect_uri parity with reddit setting

USER_AGENT = "deleteme_bot/0.1 by tunisia3507"

CLIENT_ID = os.environ['DMB_CLIENT_ID']
CLIENT_SECRET = os.environ['DMB_CLIENT_SECRET']


def get_refresh_token(one_time_code):
    reddit = get_reddit_instance()
    return reddit.auth.authorize(one_time_code)


def get_reddit_instance(user_obj=None):
    if user_obj:
        return Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            refresh_token=user_obj.refresh_token,
            user_agent=USER_AGENT
        )
    else:
        return Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=BASE_URL + reverse('deleteme_bot:auth_thanks'),
            user_agent=USER_AGENT
        )


def get_auth_url(state_code):
    reddit = get_reddit_instance()
    return reddit.auth.url(['identity', 'read', 'edit', 'history'], state_code, 'permanent')

HEADERS = {
    'user-agent': USER_AGENT,
    'user': CLIENT_ID,
    'password': CLIENT_SECRET
}


def get_headers(access_token=None):
    headers = HEADERS.copy()
    if access_token:
        headers['Authentication'] = 'bearer ' + access_token
    return headers
