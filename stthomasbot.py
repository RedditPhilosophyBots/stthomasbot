import praw, time, calendar
from summagetter import *

# Program functions
# Returns current timestamp
def now():
    return calendar.timegm(time.gmtime())

# Parse the Reddit comment
def parse(body):
    # Function variables
    endtext = "]"
    splitby = ","

    # Request made by user
    tokens = body.split(triggertext, 1)[1].split(endtext, 1)[0].split(splitby)
    return getsumma(tokens)

# Log in and monitor subs
f = open("password.txt", "r")
passwd=f.read()
reddit = praw.Reddit(user_agent='stthomasbot quotes the Summa',
                  client_id='OHbO_eTagcWcSA',
                  client_secret='i0K9lteiBqIVNOdBKBPDPpL64rg',
                  username='stthomasbot',
                  password=passwd)
subreddit = reddit.subreddit('redditphilosophybots')
starttime = now()

username = reddit.user.me()

# Main stream
print("Ready to begin quoting the Summa.")
for comment in subreddit.stream.comments():
    if triggertext in comment.body and starttime <= comment.created_utc:
        if comment.author != username: #reddit.user.me():
            print("New comment found at " + str(now()))
            response = parse(comment.body)
            #print(response)
            comment.reply(response)
            print("Wrote response at " + str(now()))
