from datetime import datetime, timezone
import re
import dateparser
from django.core.management.base import BaseCommand, CommandError
from deleteme_bot.models import StateCode, RedditUser, RedditComment, DeletemeBotSingleton
from deleteme_bot.reddit_auth import get_reddit_instance
from string import ascii_letters
import random


COMMAND_RE = re.compile('^/posts(.*?)$', re.MULTILINE)

FOOTNOTE_BASE = 'This comment will be deleted at {} UTC by [{}]({}).'

CHARACTERS = ascii_letters + '0123456789' + '\n '

config = DeletemeBotSingleton.get()


def make_footnote(delete_on):
    footnote_txt = FOOTNOTE_BASE.format(
        delete_on.isoformat(),
        config.name,
        config.url
    )
    return '\n\n ^({})'.format(footnote_txt)


def datetime_to_timestamp(dt):
    return int(dt.strftime('%s'))


def make_jargon(post_length):
    return ''.join([random.choice(CHARACTERS) for _ in range(post_length)])


class Command(BaseCommand):
    help = 'Crawls for new data'

    def handle(self, *args, **options):
        StateCode.delete_expired()
        now = self.find_new_comments_and_delete_old()

        config.last_run = now
        config.save()

    def find_new_comments_and_delete_old(self):
        now = datetime.now(timezone.utc)
        last_run = datetime_to_timestamp(config.last_run)

        for user in RedditUser.objects.all():
            try:
                reddit = get_reddit_instance(user)
                redditor = reddit.user.me()
            except:
                user.increment_strikes()
                break
            self.stdout.write("Scanning {}'s posts...".format(redditor.name))
            for comment in redditor.comments.new():
                self.stdout.write("  - reading post with ID {}".format(comment.id))

                self.stdout('comment created: {}\nlast run:        {}'.format(comment.created_utc, last_run))

                if comment.created_utc < datetime_to_timestamp(config.last_run):
                    break

                self.stdout.write("    - post is new")

                txt = comment.body
                match = COMMAND_RE.search(txt)

                if not match:
                    self.stdout.write('    - post does not contain command')
                    continue

                self.stdout.write('    - post contains command')
                command = match.groups()[0].strip()
                if command:
                    delete_on = dateparser.parse(command)
                else:
                    delete_on = now + config.default_delay

                self.stdout.write('    - post to be deleted {}'.format(delete_on.isoformat()))

                RedditComment.objects.create(user=user, comment_id=comment.id, delete_on=delete_on)

                comment.edit(txt + make_footnote(delete_on))

            for comment_instance in user.comments.filter(delete_on__lt=now):
                self.stdout.write("  - deleting post {}".format(comment_instance.comment_id))
                reddit_comment = reddit.comment(comment.comment_id)
                reddit_comment.edit(make_jargon(len(comment.body)))
                reddit_comment.delete()
                comment_instance.delete()

        return now
