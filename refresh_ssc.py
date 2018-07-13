import json
import re
import codecs
from bs4 import BeautifulSoup as Soup
import requests
import arrow
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--count', required=False)
parser.add_argument('--dl', required=False)
args = parser.parse_args()

headers = {
    "User-Agent":
    ("Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/61.0.3163.79 Safari/537.36")
    }

def make_yml(links):
    todays_date = arrow.now().format('YYYY-MM-DD')
    result = '''shortname: slatestarcodex.recent
title: SlateStarCodex Recent Posts {}
author: Scott Alexander
content:
'''.format(arrow.now().format('YYYY-MM-DD'))
    for link in links:
        result = result + '- {}?comments=false\n'.format(link)
    return result

def is_open_thread(url):
    if 'open-thread' in url or re.search('ot\d+', url):
        return True
    return False


def ssc_filter(links):
    pattern = re.compile("\d+\/\d+\/\d+")
    results = []
    for link in links:
        if re.search(pattern, link):
            if not is_open_thread(link):
                results.append(link)
    return results

def get_links(url):
    r = requests.get(url, headers=headers)
    soup = Soup(r.text, "html.parser")
    links = []
    for a in soup.find_all('a'):
        link = a.get('href')
        if link:
            if link not in links:
                links.append(link)
    return links


def prepare_links(download=False):
    url = "http://slatestarcodex.com/archives/?comments=false"
    if download:
        print('Refreshing download')
        links = get_links(url)
        links = ssc_filter(links)
        #
        with open('archive.json','w') as f:
            f.write(json.dumps(links, indent=2, sort_keys=True))
    else:
        print('Using archive')
        with open('archive.json') as f:
            links = json.loads(f.read())
    return links

count = args.count or 30
dl = args.dl or False
print(dl)

links = prepare_links(download=dl)
#
with open('definitions/slatestarcodex.recent.yml','w') as f:
    recent_links = list(reversed(links[:count]))
    # print('\n'.join(recent_links))
    f.write(make_yml(recent_links))
