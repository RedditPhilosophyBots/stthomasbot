import praw, time, calendar, html2text, urllib2

##########
# Summa Citation Convention:
# ST Part, Questions, Article, Article Subsection
FirstPart = "I"
FirstPartofSecondPart = "I-II"
SecondPartoftheSecondPart = "II-II"
ThirdPart = "III"
Supplement = "Suppl."
# pr. prologue to a question
prologue = "pr."
# arg. objections
objections = "arg."
# s.c. On the contrary
contrary = "s.c."
# co. I respond that
Isay = "co."
# ad. replies to objections
reply = "ad."
#
# Example:
# ST I-II, Q3, A2, ad.1
# First Part of the Second Part, Question 3, Article 2, Reply to objection 1
##########

# Program variables
triggertext = "[*ST*"
h = html2text.HTML2Text()
error="error"
pageext=".htm"


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

# Get the correct excerpt from the Summa
def getsumma(tokens):
	# Function Variables
	titlestartchar = "<h1>"
	titleendchar = "</h1>"

	# Get the page source back
	page = getlink(tokens)
	if page == "error":
		return "Error Message."

	# Grab the question
	question = "# " + page.split(titlestartchar)[1].split(titleendchar)[0] + "\n\n"
	return str(question)

# Grab the correct link given the tokens.
def getlink(tokens):
	link = "http://www.newadvent.org/summa/"
	question = ""
	qnum = 0

	# Find Summa Part
	if tokens[0].split(" ")[1] == FirstPart:
		link = link + "1"
	elif tokens[0].split(" ")[1] == FirstPartofSecondPart:
		link = link + "2"
	elif tokens[0].split(" ")[1] == SecondPartoftheSecondPart:
		link = link + "3"
	elif tokens[0].split(" ")[1] == ThirdPart:
		link = link + "4"
	elif tokens[0].split(" ")[1] == Supplement:
		link = link + "5"
	else:
		return error

	# Find Question
	if "Q" in tokens[1]:
		question = tokens[1].split("Q")[1]
	else:
		return error
	try:
		qnum = int(question)
	except:
		return error
	if qnum < 1:
		return error
	elif qnum < 10:
		link = link + "00" + str(qnum) + pageext
	elif qnum < 100:
		link = link + "0" + str(qnum) + pageext
	else:
		link = link + str(qnum) + pageext

	# Grab link
	print("Getting: " + link)
	response = urllib2.urlopen(link)
	pagesource = response.read()
	if "404 Not Found" in pagesource:
		return error
	else:
		return pagesource


# Log in and monitor subs
f = open("password.txt", "r")
reddit = praw.Reddit(user_agent='stthomasbot quotes the Summa',
                  client_id='aeEGPm_mikBDAg',
                  client_secret='cR2cBWWE6BG7eoPA8qSdzf6eCeU',
                  username='stthomasbot',
                  password=f.read())
subreddit = reddit.subreddit('redditphilosophybots')
starttime = now()


# Main stream
print("Ready to begin quoting the Summa.")
for comment in subreddit.stream.comments():
	if comment.author != reddit.user.me():
		if triggertext in comment.body and starttime <= comment.created_utc:
			print("New comment found at " + str(now()))
			response = parse(comment.body)
			comment.reply(response)
			print("Wrote response at " + str(now()))
			print(response)