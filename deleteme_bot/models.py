from django.db import models
from datetime import timedelta, datetime


class AppConfiguration(models.Model):
    id = models.IntegerField(primary_key=True, default=1)
    last_run = models.DateTimeField(default=datetime.utcnow())
    name = models.CharField(max_length=20, default='deleteme_bot')
    default_delay = models.DurationField(default=timedelta(days=7))
    url = models.URLField(default='https://github.com/clbarnes/deleteme_bot')

    @classmethod
    def get(cls):
        return cls.objects.get(pk=1)


class RedditUser(models.Model):
    # username = models.CharField(max_length=20, unique=True)  # privacy reasons
    # access_token = models.CharField(max_length=30, help_text='Use RedditUser.get_valid_token() to get this.')
    # expires = models.DateTimeField()
    refresh_token = models.CharField(max_length=30, unique=True)
    # latest_post = models.DateTimeField(default=datetime.utcnow())
    # delete_all = models.BooleanField(default=False)
    # default_lapse = models.DurationField(default=timedelta(days=7))

    # def get_valid_token(self):
    #     if datetime.utcnow() >= self.expires:
    #         access_token, expires = refresh_auth(self.refresh_token)
    #         self.access_token = access_token
    #         self.expires = expires
    #
    #     return self.access_token


class RedditComment(models.Model):
    user = models.ForeignKey(RedditUser, on_delete=models.CASCADE, related_name='comments')
    comment_id = models.CharField(max_length=10, help_text='Do not include type prefix', unique=True)
    delete_on = models.DateTimeField()


class StateCode(models.Model):
    state_code = models.CharField(max_length=30, unique=True)
    expires = models.DateTimeField(default=datetime.utcnow() + timedelta(hours=1))

    @classmethod
    def delete_expired(cls):
        cls.objects.filter(expires__lt=datetime.utcnow()).delete()

    @classmethod
    def exists(cls, state_code):
        return cls.objects.filter(state_code=state_code).exists()
