import praw, time, calendar, sys
from summagetter import *

botname = "stthomasbot"
iamabot = "\n\n---\n\n^I ^am ^a ^bot ^and ^this ^operation ^was ^performed ^automatically."
mysubs = "redditphilosophybots+catholicism"
dev = 1

# Program functions
# Returns current timestamp
def now():
    return calendar.timegm(time.gmtime())

# Parse the Reddit comment
def parse(body):
    # Function variables
    endtext = "]"
    splitby = ","

    # One or more requests made by user
    listOfTokenSets = list()
    for triggertext in triggertexts: 
    # This solution has the downside of returning multiple cites ordered by 
    # source, rather than in the order the cited are recited in the comment.  
    # I think the solution may require either more complicated for loops or
    # a recursive function
        tempbody = body
        while triggertext in tempbody:
            tokens = [triggertext] + tempbody.split(triggertext, 1)[1].split(endtext, 1)[0].split(splitby)
            listOfTokenSets.append(tokens)
            tempbody = tempbody.split(triggertext, 1)[1].split(endtext, 1)[1]
    return getsumma(listOfTokenSets)

# Catch any errors and re-authenticate bot
flag = 1

while 1:
    try:
        if flag == 1:
            flag = 0
            # Log in and monitor subs
            subreddit = ""
            reddit = praw.Reddit(botname, user_agent='stthomasbot quotes the Summa')
            if dev == 1:
                subreddit = reddit.subreddit('redditphilosophybots')
            else:
                print(mysubs)
                subreddit = reddit.subreddit(mysubs)
            starttime = now()

            username = reddit.user.me()

            # Main stream
            print("Ready to begin quoting the Summa.")
            for comment in subreddit.stream.comments():
                for triggertext in triggertexts:
                    if triggertext in comment.body and starttime <= comment.created_utc:
                        if comment.author != username:
                            print("New comment found at " + str(now()))
                            response = parse(comment.body)
                            comment.reply(response + iamabot)
                            print("Wrote response at " + str(now()))
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()
    except:
        print("There was an error. Restarting...")
        flag = 1