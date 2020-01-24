import urllib.request, html2text, traceback

##########
# Summa Citation Convention:
# ST Part, Questions, Article, Article Subsection
FirstPart = "I"
FirstPartofSecondPart = "I-II"
SecondPartoftheSecondPart = "II-II"
ThirdPart = "III"
Supplement = "Suppl."
# arg. objections
objections = "arg."
# s.c. On the contrary
contrary = "s.c."
# co. I respond that
isay = "co."
# ad. replies to objections
reply = "ad."
#
# Example:
# ST I-II, Q3, A2, ad.1
# First Part of the Second Part, Question 3, Article 2, Reply to objection 1
##########

# Program variables
triggertexts = ["[ST", "[SCG", "[straw"]
error="error"
pageext=".htm"

# Get the correct excerpt from the Summa
def getsumma(listOfTokenSets):
    # Function Variables
    titlestartchar = "<h1>"
    titleendchar = "</h1>"
    questionstartchar = "</a></em></p>"
    questionendchar = "<table"
    articleSplit = "<h2 id=\"article"
    articleHeaderEnd = "</h2>"
    errormessage = """# Uh oh, something went wrong. Check your formatting. Your text should match the following convention:

[ST I, Q2, A3, co.]

In citations, co., arg., ad., and s.c. are optional specifications. Q and A are required. This means that [ST I, Q2, A3] is a valid citation.

1. Double check that you've referred to a valid part of the Summa.

2. Does your article contain the objection you referenced?

3. Does your question contain the article you referenced?

4. Does your question exist?

5. Did you cite the part of the summa correctly (The supplemental part is only recognized as Suppl., not III-II)?

6. Do you have spaces between the Q and A and their corresponding numbers? Or arg. and ad. and their corresponding numbers?

[Message /u/jared_dembrun](https://www.reddit.com/message/compose/?to=jared_dembrun&subject=StThomasBot) if you think this message was my fault and not due to formatting. Please include a link to your comment in the message, but [please don't lie](https://i.pinimg.com/originals/73/d6/93/73d693021693ef9c1119db4079717321.jpg)."""

    post = ""

    for tokenSet in listOfTokenSets:

        # Return an error if we run into an exception instead of completing without error.
        try:
            # Get the page source back
            if tokenSet[0] == "[ST":
                tokenSet = tokenSet[1:]
                page = getSummaTheologicalLink(tokenSet)
                if page == error:
                    print("Error getting link.")
                    return errormessage

                # Grab the question
                question = "# " + page.split(titlestartchar)[1].split(titleendchar)[0] + "\n\n"

                # Grab the question text
                questiontext = page.split(questionstartchar)[1].split(questionendchar)[0]

                # Get the article
                if "A" in tokenSet[2]:
                    articleNum = tokenSet[2].split("A")[1]
                else:
                    print("No specified article: not allowed.")
                    return errormessage

                # Split on article number and append <h2> to front.
                articleText = ""
                articleText = "<h2" + questiontext.split(articleSplit  + str(articleNum) + "\"")[1].split(articleSplit)[0]


                # If posting full article, skip this
                if not len(tokenSet) == 3:
                    subsection = getsubsection(articleText, tokenSet)
                    if subsection == error:
                        print("Error on subsection.")
                        return errormessage
                    else:
                        articleText = "<h2" + questiontext.split(articleSplit  + str(articleNum) + "\"")[1].split(articleHeaderEnd)[0] + subsection

                # Ready question text for reddit posting
                h = html2text.HTML2Text()
                h.ignore_links = True
                post += question + h.handle(articleText)
                h.close()
            elif tokenSet[0] == "[SCG":
                page = getSummaContraGentilesLink(tokenSet[1:])
                post += page
            elif tokenSet[0] == "[straw":
                post += ">I adjure you by the living almighty God, and by the faith you have in our order, and by charity that you strictly promise me you will never reveal in my lifetime what I tell you. Everything that I have written seems like straw to me compared to those things that I have seen and have been revealed to me. - Thomas Aquinas, December 6, AD 1273\n\n"

        except:
            traceback.print_exc()
            print("End of error traceback\n\n")
            return errormessage

    return breakuppostlen(post)


def breakuppostlen(post):
    chunk = 9500
    reply = list()
    if len(post) < chunk:
        reply.append(str(post))
        return reply
    else:
        print("Message too long, breaking into multiple comments")
        for i in range(0, ((len(post)/chunk)+1)):
            print(str(i) + "th break")
            reply.append(post[:chunk])
            post = post[chunk:]
            print("Length of next chunk = " + str(len(post)))
        return reply


# Grab the correct link given the tokens.
def getSummaTheologicalLink(tokens):
    link = "http://www.newadvent.org/summa/"
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
    qnum = int(question)
    if qnum < 1 or qnum > 999:
        return error
    else:
        link = link + '{0:03}'.format(qnum) + pageext #format qnum as a zero-padded string of width 3

    # Grab link
    print("Getting: " + link)
    try:
        response = urllib.request.urlopen(link)
        pagesource = response.read()
        return pagesource
    except urllib2.HTTPError as e:
        if e.code == '404':
            return "404 error"
    except Exception as e:
        return error

def getsubsection(text, tokens):
    objstart = "<p><strong>Objection "
    contrastart = "<p><strong>On the contrary"
    answerstart = "<p><strong>I answer that"
    replystart = "<p><strong>Reply to Objection "
    nextsub = "<p><strong>"
    if objections in tokens[3]:
        objnum = tokens[3].split(objections)[1]
        return objstart + str(objnum) + text.split(objstart + objnum)[1].split(nextsub)[0]
    elif contrary in tokens[3]:
        return contrastart + text.split(contrastart)[1].split(nextsub)[0]
    elif isay in tokens[3]:
        return answerstart + text.split(answerstart)[1].split(nextsub)[0]
    elif reply in tokens[3]:
        replynum = tokens[3].split(reply)[1]
        return replystart + str(replynum) + text.split(replystart + replynum)[1].split(nextsub)[0]
    else:
        return error

def getSummaContraGentilesLink(tokens):
    return "Sorry, but Summa Contra Gentiles functionality is not yet included\n\n"
