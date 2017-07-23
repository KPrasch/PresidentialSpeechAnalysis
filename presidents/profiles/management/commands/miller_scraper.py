import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import os


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
    links = sorted({a['href'] for a in little_soup})
    return links


def scrape(links: list):
    """

    :param links:
    :return:
    """
    speeches = dict()
    for slink in links:
        url = BASE_URL + slink
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        try:
            president = soup.article.h2.text
            little_soup = soup.find('div', {"id": "transcript"})
            transcript = little_soup.text

            title = soup.article.h1.text
            date_string = title.split('(')[-1].replace(')', '')
            date = datetime.strptime(date_string, "%B %d, %Y")

        except AttributeError:
            print("Skipping {url}".format(url=url))

        else:
            speechdata = {'name': president,
                          'title': title,
                          'date': date,
                          'transcript': transcript}
            try:
                speeches[president].append(speechdata)
            except KeyError:
                speeches[president] = [speechdata]

    return speeches
