import urllib
import io
from BeautifulSoup import BeautifulSoup
import validators

CRAWLED_DATA_PATH = "data/crawled/"

html = []

def isUrlDomain(url):
    # Todo: Implement domain checker
    return True

def save(url, raw_html):
    modified_url = url.replace("/", "\\")
    file = open("../" + CRAWLED_DATA_PATH + modified_url + ".html", "w")
    print "going"
    file.write(BeautifulSoup.prettify(raw_html))
    file.close()

def visit(url, filter):
    valid_links = []

    handler = urllib.urlopen(url)
    raw_html = BeautifulSoup(handler)

    # Save data
    save(url, raw_html)

    # Find URLs it points to
    atags = raw_html.findAll('a')
    print "found ", len(atags), "tags"
    for tag in atags:
        link = tag.get('href')
        is_url = True
        if not validators.url(link):
            is_url = False
        if is_url & filter & isUrlDomain(link):
            valid_links.append(link)

    return valid_links

# Basic script

# Todo: Add command line arguments

# Todo: Get the domain of the seed
domain = "vagalume"
seed = "https://www.vagalume.com.br/"
visited_urls = []
visit_queue = [seed]
filter_urls = True

while(len(visit_queue) > 0):
    current_url = visit_queue[0]
    visit_queue.pop(0)

    if current_url in visited_urls:
        continue

    visited_urls.append(current_url)

    # Todo: Add module to avoid overload

    # Visit url
    print "Visit ", current_url
    try:
        next_urls = visit(current_url, filter_urls)
        visit_queue += next_urls
    except IOError as e:
        print "Could not reach the website! :("
        print e
    except:
        print "Unknown error - Something went wrong! :O"
