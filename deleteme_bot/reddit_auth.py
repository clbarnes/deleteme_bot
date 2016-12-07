from praw import Reddit
import requests
import json
from django.urls import reverse

with open('app_credentials.json') as f:
    app_credentials = json.load(f)

REDIRECT_URI = "http://www.example.com/unused/redirect/uri"  # todo

USER_AGENT = "t3507_deleter/0.1 by tunisia3507"

# AUTH_URL_BASE = "https://www.reddit.com/api/v1/authorize?" + \
#                 "client_id={client_id}" + \
#                 "&response_type=code" + \
#                 "&state={state}" + \
#                 "&redirect_uri={redirect_uri}" + \
#                 "&duration=permanent" + \
#                 "&scope=edit".format(
#                     client_id=app_credentials['client_id'],
#                     redirect_uri=reverse('deleteme_bot:landing')
#                 )


def get_refresh_token(one_time_code):
    # reddit = Reddit(
    #     client_id=app_credentials['client_id'],
    #     client_secret=app_credentials['client_secret'],
    #     redirect_uri=reverse('deleteme_bot:landing'),
    #     user_agent=USER_AGENT
    # )
    reddit = get_reddit_instance()
    return reddit.auth.authorize(one_time_code)


def get_reddit_instance(user_obj=None):
    if user_obj:
        return Reddit(
            client_id=app_credentials['client_id'],
            client_secret=app_credentials['client_secret'],
            refresh_token=user_obj.refresh_token,
            user_agent=USER_AGENT
        )
    else:
        return Reddit(
            client_id=app_credentials['client_id'],
            client_secret=app_credentials['client_secret'],
            user_agent=USER_AGENT
        )


def get_auth_url(state_code):
    reddit = Reddit(
            client_id=app_credentials['client_id'],
            client_secret=app_credentials['client_secret'],
            redirect_uri=reverse('deleteme_bot:landing'),
            user_agent=USER_AGENT
        )
    return reddit.auth.url(['edit'], state_code, 'permanent')

HEADERS = {
    'user-agent': USER_AGENT,
    'user': app_credentials['client_id'],
    'password': app_credentials['client_secret']
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

if __name__ == '__main__':
    print(1+1)