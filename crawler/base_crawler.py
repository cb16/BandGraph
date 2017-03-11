import urllib
import io
import os
from BeautifulSoup import BeautifulSoup
import validators
import tldextract
from time import time

CRAWLED_DATA_PATH = "/data/crawled/"
PROJECT_DIR = os.getcwd()
TIME_INTERVAL = 0.01

# Todo: Add command line arguments

seed = "https://www.vagalume.com.br/"
domain = tldextract.extract(seed).domain
visited_urls = []
visit_queue = [seed]
filter_urls = True
last_visit = time()

def isUrlDomain(url):
    urlDomain = tldextract.extract(url).domain
    if urlDomain != domain:
        return False
    return True

def save(url, raw_html):
    modified_url = url.replace("/", "|")
    file = open(PROJECT_DIR + CRAWLED_DATA_PATH + modified_url + ".html", "w")
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

while(len(visit_queue) > 0):
    current_url = visit_queue[0]
    visit_queue.pop(0)

    if current_url in visited_urls:
        continue

    current_time = time()
    if current_time - last_visit < TIME_INTERVAL:
        visit_queue.append(current_url)
        print "Time interval not reached. Will visit later."
        continue

    visited_urls.append(current_url)

    # Visit url
    print "Visit ", current_url
    last_visit = time()
    try:
        next_urls = visit(current_url, filter_urls)
        visit_queue += next_urls
    except IOError as e:
        print "Could not reach the website! :("
        print e
    except:
        print "Unknown error - Something went wrong! :O"
