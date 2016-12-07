# deleteme_bot

deleteme_bot is a reddit bot which users can ask to delete any of their 
posts.

## Usage

Firstly, you need to give the bot permission to delete your posts. To do
so, please [click this link](a/url/here).

Then just add `/deleteme` to any of your posts on its own line and the
post will be deleted in 7 days.

For more granular control, type a date, time or interval after 
`/deleteme`, for example `/deleteme tomorrow`, `/deleteme next Tuesday`,
or `/deleteme on 09/25/18`.
The bot uses the [dateparser](https://pypi.python.org/pypi/dateparser)
library to interpret these dates and so works in multiple languages!
Times are interpreted in UTC, but regrettably assumes the US 
`MM/DD/YYYY` format for dates.

## Security

This bot requires the 'edit' privilege. This means that it can delete
or edit any of your posts, which sounds like a big deal. However, each 
access token is only valid for 60 minutes and the app secret is required
to refresh it - so a hacker would need both the database dump *and*
access to my file system to get edit privileges on your account.

I also don't store usernames (although I do use the API to find it out 
so that I can search your posts for `/deleteme`).