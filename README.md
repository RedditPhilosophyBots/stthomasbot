# stthomasbot

## Running the Project

After cloning the reposiitory and adding a configured praw.ini, simply run `python stthomasbot.py`. The program will run indefinitely.

## HTML 2 Text

The `html2text.py` file is borrowed from [another open source project](https://github.com/aaronsw/html2text). The module converts html to markdown.

## Example Trigger Text

Post a comment to the `/r/redditphilosophybots` subreddit which contains the text `[*ST* I-II, Q3, A2, ad.2]`

## Authentication

Add a `praw.ini` file with the following configuration:

    [default]
    client_id=
    client_secret=
    username=
    password=
