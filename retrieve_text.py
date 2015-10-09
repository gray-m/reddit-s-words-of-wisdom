from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
import urllib
import time
import sys

# counters for testing
num_comments = 0
pages_visited = 0
# global lists
text_data = []
page_urls = []

# get links to the comments
def find_comment_links(html_doc):
    comment_links = []
    parsed = BeautifulSoup(html_doc, 'html.parser').find_all('a', {'class':'comments may-blank'})
    for link in parsed:
        comment_links.append(link.get('href'))
    return comment_links


# get the text from the comment pages
def get_comment_text(html_doc):
    global num_comments
    comments_text = []
    comment_div = BeautifulSoup(html_doc, 'html.parser').find('div', {'class':'commentarea'})
    if(comment_div is not None):
        comments = comment_div.find_all('div', {'class':'usertext-body may-blank-within md-container '})
        for div in comments:
            md_divs = div.find_all('div', {'class':'md'})
            for md_div in md_divs:
                ps = md_div.find_all('p')
                for p in ps:
                    comments_text.append(p.get_text())
                    num_comments = num_comments + 1
    return comments_text

# get url of the page ref'd by the next button
def get_next_page_url(html_doc):
    a_tag = BeautifulSoup(html_doc, 'html.parser').find('a', {'rel':'nofollow next'})
    return a_tag.get('href')

# get comment text
def get_all_comments(url):
    global text_data, num_comments, pages_visited
    page_html = urllib.urlopen(url).read()
    comment_links = find_comment_links(page_html)
    for link in comment_links:
        standardized = standardize_text(link)
        pages_visited = pages_visited + 1
        raw = urllib.urlopen(standardized).read()
        text_data.append(get_comment_text(raw))
        # so reddit doesn't yell at me
        time.sleep(.75)
    print ("Went to {0} pages and got {1} comments!".format(pages_visited,num_comments))
    pages_visited = 0
    num_comments = 0

# in case the urls have special characters
def standardize_text(text):
    u = text.encode('utf-8')
    return u

# for testing
sub = sys.argv[1]

# because zero-base indexing
num_pages = int(sys.argv[2]) - 1

# should really rename this script something to do with reddit
url = 'https://www.reddit.com/r/' + sub
page_urls.append(url)

# get urls for all the pages to search
for i in xrange(0, num_pages):
    page_urls[i] = standardize_text(page_urls[i])
    page_data = urllib.urlopen(page_urls[i]).read()
    page_urls.append(get_next_page_url(page_data))
    # so reddit definitely won't yell at me
    time.sleep(.5)

# get text from the comments
for link in page_urls:
    print ("going to {0}...".format(link))
    get_all_comments(link)
    # more reddit yelling prevention
    time.sleep(2)

f = open(sub,'w')
for text in text_data:
    for line in text:
        f.write(standardize_text(line) + '\n')
f.close()
