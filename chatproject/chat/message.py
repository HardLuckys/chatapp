import re

def message_cheker(message):
    if link(message) == False:
        matches = message
    else:
        matches = link(message)  
    return str(matches)

def link(message):
    try:
        link = re.search("(?P<url>https?://[^\s]+)", message).group("url")
        matches = '<a href="' + link + '">' + link.split("//")[-1].split("/")[0] + '</a>'
    except:
        matches = False
    return matches

def emoji(message):
    try:
        link = re.search("(?P<url>https?://[^\s]+)", message).group("url")
        matches = '<a href="' + link + '">' + link.split("//")[-1].split("/")[0] + '</a>'
    except:
        matches = False
    return matches


#print(message_cheker('message, http://wwww.google.com/'))
