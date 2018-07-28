import urllib2, html2text

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
triggertext = "[*ST*"
error="error"
pageext=".htm"

# Get the correct excerpt from the Summa
def getsumma(tokens):
    # Function Variables
    titlestartchar = "<h1>"
    titleendchar = "</h1>"
    questionstartchar = "</a></em></p>"
    questionendchar = "<table"
    articleSplit = "<h2 id=\"article"
    articleHeaderEnd = "</h2>"

    # Get the page source back
    page = getlink(tokens)
    if page == error:
        return "Error Message."

    # Grab the question
    question = "# " + page.split(titlestartchar)[1].split(titleendchar)[0] + "\n\n"

    # Grab the question text
    questiontext = page.split(questionstartchar)[1].split(questionendchar)[0]

    # Get the article
    if "A" in tokens[2]:
        articleNum = tokens[2].split("A")[1]
    else:
        return error

    # Split on article number and append <h2> to front.
    articleText = ""
    print("ArticleText1: " + articleText)
    articleText = "<h2" + questiontext.split(articleSplit  + str(articleNum) + "\"")[1].split(articleSplit)[0]
    print("ArticleText2: " + articleText)


    # If posting full article, skip this
    if not len(tokens) == 3:
        print("\n\nGetting sub part\n\n")
        articleText = "<h2" + questiontext.split(articleSplit  + str(articleNum) + "\"")[1].split(articleHeaderEnd)[0] + getsubpart(articleText, tokens)

    print("ArticleText3: " + articleText)

    # Ready question text for reddit posting
    h = html2text.HTML2Text()
    h.ignore_links = True
    post = question + h.handle(articleText)
    h.close()

    print(post)

    return str(post)

# Grab the correct link given the tokens.
def getlink(tokens):
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

def getsubpart(text, tokens):
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
