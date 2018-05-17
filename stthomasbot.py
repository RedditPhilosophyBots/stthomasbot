import praw, time, calendar, html2text, urllib2

# Program variables
starttime = calendar.timegm(time.gmtime())
triggertext = "[*ST*"
h = html2text.HTML2Text()

def parse(body):
	# Function variables
	endtext = "]"
	titlestartchar = "<h1>"
	titleendchar = "</h1>"

	# Request made by user
	request = body.split(triggertext, 1)[1].split(endtext, 1)[0]
	return request

reddit = praw.Reddit(user_agent='stthomasbot quotes the Summa',
                  client_id='aeEGPm_mikBDAg',
                  client_secret='cR2cBWWE6BG7eoPA8qSdzf6eCeU',
                  username='stthomasbot',
                  password='')

subreddit = reddit.subreddit('redditphilosophybots')

for comment in subreddit.stream.comments():
	if comment.author != reddit.user.me():
		if triggertext in comment.body and starttime <= comment.created_utc:
			print("New comment found! Parsing...")
			comment.reply(parse(comment.body))