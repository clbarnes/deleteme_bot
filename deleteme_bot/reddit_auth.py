import os
from praw import Reddit
import requests
from django.urls import reverse

# todo
BASE_URL = 'http://localhost:8000'  # to allow redirect_uri parity with reddit setting

USER_AGENT = "deleteme_bot/0.1 by tunisia3507"

CLIENT_ID = os.environ['DMB_CLIENT_ID']
CLIENT_SECRET = os.environ['DMB_CLIENT_SECRET']

# AUTH_URL_BASE = "https://www.reddit.com/api/v1/authorize?" + \
#                 "client_id={client_id}" + \
#                 "&response_type=code" + \
#                 "&state={state}" + \
#                 "&redirect_uri={redirect_uri}" + \
#                 "&duration=permanent" + \
#                 "&scope=edit".format(
#                     client_id=CLIENT_ID,
#                     redirect_uri=reverse('deleteme_bot:landing')
#                 )


def get_refresh_token(one_time_code):
    # reddit = Reddit(
    #     client_id=CLIENT_ID,
    #     client_secret=CLIENT_SECRET,
    #     redirect_uri=reverse('deleteme_bot:landing'),
    #     user_agent=USER_AGENT
    # )
    reddit = get_reddit_instance()
    return reddit.auth.authorize(one_time_code)


def get_reddit_instance(user_obj=None):
    if user_obj:
        return Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            # refresh_token=refresh_token,
            refresh_token=user_obj.refresh_token,
            user_agent=USER_AGENT
        )
    else:
        return Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            # redirect_uri=reverse('deleteme_bot:auth_thanks'),
            redirect_uri=BASE_URL + reverse('deleteme_bot:auth_thanks'),
            user_agent=USER_AGENT
        )


def get_auth_url(state_code):
    reddit = get_reddit_instance()
    return reddit.auth.url(['identity', 'edit'], state_code, 'permanent')

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
#
#
# def get_first_auth(code):
#     """
#     :param code: One-time use code for authentication
#     :return: access_token str, refresh_token str, expires datetime
#     """
#     reddit = get_reddit_instance()
#     refresh_token = reddit.auth.authorize(code)
#     username = reddit.user.me()
#
#     return code, refresh_token, username
#
#
# def get_username(refresh_token):
#     reddit = get_reddit_instance(refresh_token)
#     return reddit.user.me()


def delete_post(access_token, post_id):
    requests.post(
        'https://oauth.reddit.com/api/del',
        {'id': 't1_' + post_id},
        headers=get_headers(access_token)
    )


def revoke_token(access_token):
    response = requests.post(
        'https://www.reddit.com/api/v1/revoke_token',
        {'token': access_token, 'token_type_hint': 'access_token'},
        headers=get_headers(access_token)
    )

    return response.status_code == 204
