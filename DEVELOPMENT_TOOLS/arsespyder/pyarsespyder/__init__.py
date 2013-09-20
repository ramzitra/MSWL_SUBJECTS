from bs4 import BeautifulSoup as Soup
import geturl

def print_urls(url):
    text = geturl.urlToString(url)
    try:
        s = Soup(text)
        return [x['href'] for x in s.findAll('a', href=True)]
    except:
        print "ERROR ON SOUP CREATION"
        return []
