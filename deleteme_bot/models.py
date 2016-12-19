from django.db import models
from django.core.exceptions import ObjectDoesNotExist
import os
from datetime import timedelta, datetime, timezone


MAX_STRIKES = 5

class DeletemeBotSingleton(models.Model):
    id = models.IntegerField(primary_key=True)
    last_run = models.DateTimeField()
    name = models.CharField(max_length=20)
    default_delay = models.DurationField()
    url = models.URLField()

    class Meta:
        app_label = 'deleteme_bot'
        db_table = 'deleteme_bot_singleton'

    @classmethod
    def get(cls):
        try:
            return cls.objects.get(pk=1)
        except ObjectDoesNotExist:
            cls.objects.create(
                id=1,
                name=os.environ['DMB_NAME'],
                last_run=datetime.now(timezone.utc),
                default_delay=timedelta(seconds=int(os.environ['DMB_DEFAULT_DELAY'])),
                url=os.environ['DMB_URL']
            )

        return cls.objects.get(pk=1)


class RedditUser(models.Model):
    refresh_token = models.CharField(max_length=80, unique=True)
    strikes = models.IntegerField(default=0)

    class Meta:
        app_label = 'deleteme_bot'
        db_table = 'reddit_user'

    def increment_strikes(self):
        self.strikes = models.F('strikes') + 1
        self.save()

    @classmethod
    def delete_revoked(cls):
        cls.objects.filter(strikes__gte=MAX_STRIKES).delete()


class RedditComment(models.Model):
    user = models.ForeignKey(RedditUser, on_delete=models.CASCADE, related_name='comments')
    comment_id = models.CharField(max_length=10, help_text='Do not include type prefix', unique=True)
    delete_on = models.DateTimeField()

    class Meta:
        app_label = 'deleteme_bot'
        db_table = 'reddit_comment'


class StateCode(models.Model):
    state_code = models.CharField(max_length=80, unique=True)
    expires = models.DateTimeField(default=datetime.now(timezone.utc) + timedelta(hours=1))

    class Meta:
        app_label = 'deleteme_bot'
        db_table = 'state_code'

    @classmethod
    def delete_expired(cls):
        cls.objects.filter(expires__lt=datetime.now(timezone.utc)).delete()

    @classmethod
    def exists(cls, state_code):
        return cls.objects.filter(state_code=state_code).exists()
