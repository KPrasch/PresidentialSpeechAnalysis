import os
import re
from datetime import datetime
from ssl import SSLError

import requests
from bs4 import BeautifulSoup
from requests.exceptions import SSLError as RequestsSSLError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR, 'commands')

BASE_URL = "http://millercenter.org/"
SPEECH_BASE_URL = 'http://millercenter.org/president/speeches/'
SEED_DATA = os.path.join(BASE_DIR, 'links.html')


def get_speech_links(seed=False):
    """Scrapes a list of links to speeches"""
    if seed:
        with open(SEED_DATA, 'r') as f:
            text = f.read()
    else:
        r = requests.get(SPEECH_BASE_URL)
        text = r.text

    soup = BeautifulSoup(text, 'html.parser')
    little_soup = soup.find_all("a", {"href": re.compile("speeches")})
    for a in little_soup:
        yield a['href']


def scrape(seed=False):
    """

    :param links:
    :return:
    """
    counter, skipped = 0, 0
    for slink in get_speech_links(seed=seed):  # TODO
        url = slink
        try:
            resp = requests.get(url)
        except (SSLError, RequestsSSLError):
            skipped += 1
            print(f'Skip: SSL Problem')
            print(f'{url}')
            continue

        soup = BeautifulSoup(resp.text, 'html.parser')
        try:
            president = soup.find('p', {'class': 'president-name'}).text.replace('\'', '')
        except AttributeError:
            print('Skip: Cannot find president name.')
            print(f'{url}')
            skipped += 1
            continue

        little_soup = soup.find('div', {"class": re.compile(r'transcript', re.I)})
        if little_soup:
            transcript = '\n'.join(p.text for p in little_soup.find_all('p') if len(p.text) >= 1)
        else:
            print(f'Skip: No transcript found.')
            print(f'{url}')
            skipped += 1
            continue

        try:
            title = soup.find('div', {'class': re.compile(r'field-title')}).a.text
        except AttributeError:
            skipped += 1
            print(f'Skip: Cannot find title.')
            print(f'{url}')

        date_string = title.split(':')[0]
        date = datetime.strptime(date_string, "%B %d, %Y").date()

        speechdata = {'speaker': president,
                      'title': title,
                      'url': url,
                      'date': date,
                      'transcript': transcript}

        yield speechdata, skipped

