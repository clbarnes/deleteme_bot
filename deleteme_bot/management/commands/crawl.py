from datetime import datetime
import re
import dateparser
from django.core.management.base import BaseCommand, CommandError
from deleteme_bot.models import StateCode, RedditUser, RedditComment, DeletemeBotSingleton
from deleteme_bot.reddit_auth import get_reddit_instance


COMMAND_RE = re.compile('^/posts(.*?)$', re.MULTILINE)

FOOTNOTE_BASE = 'This comment will be deleted at {} UTC by [{}]({}).'

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


def find_new_comments_and_delete_old():
    now = datetime.utcnow()

    for user in RedditUser.objects.all():
        reddit = get_reddit_instance(user)
        redditor = reddit.user.me()
        for comment in redditor.comments.new():
            if comment.created_utc < datetime_to_timestamp(config.last_run):
                break

            txt = comment.body
            match = COMMAND_RE.search(txt)

            if not match:
                continue

            command = match.groups()[0].strip()
            if command:
                delete_on = dateparser.parse(command)
            else:
                delete_on = now + config.default_delay

            RedditComment.objects.create(user=user, comment_id=comment.id, delete_on=delete_on)

            comment.edit(txt + make_footnote(delete_on))

        for comment in user.comments.filter(delete_on__lt=now):
            reddit.comment(comment.comment_id).delete()
            comment.delete()

    return now


def main():
    StateCode.delete_expired()
    now = find_new_comments_and_delete_old()

    config.last_run = now
    config.save()


class Command(BaseCommand):
    help = 'Crawls for new data'

    def handle(self, *args, **options):
        main()


if __name__ == '__main__':
    main()
