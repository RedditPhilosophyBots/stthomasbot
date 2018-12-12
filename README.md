# stthomasbot

## What does this do?

The stthomasbot monitors all comments on specified subreddits and responds to any comment containing the trigger text, `[ST`, which appears on Reddit as ST

With a *Summa* part, question, and article specified, the bot responds with the appropriate citation. Further refinement of the citation is possible through mentioning the article subsections.

See the [Wiki](https://github.com/RedditPhilosophyBots/stthomasbot/wiki/Intended-Use) for detailed use information.

## Running the Project

After cloning the reposiitory and adding a configured praw.ini, simply run `python stthomasbot.py`. The program will run indefinitely.

## HTML 2 Text

The `html2text.py` file is borrowed from [another open source project](https://github.com/aaronsw/html2text). The module converts html to markdown.

## Example Trigger Text

Post a comment to the `/r/redditphilosophybots` subreddit which contains the text `[ST I-II, Q3, A2, ad.2]`. This subreddit is intended for bot testing.

## Authentication

Add a `praw.ini` file with the following configuration:

    [stthomasbot]
    client_id=
    client_secret=
    username=
    password=
