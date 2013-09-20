import urllib2

def urlToString(url):
    try:
        opened = urllib2.build_opener()
        # Get the string 
        string = opened.open(url).read()
    except (urllib2.URLError, urllib2.HTTPError, ValueError):
        return ""
    return string
