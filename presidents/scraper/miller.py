from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from profiles.models import President, Speech


class PresidentSpeechLinkScraper:
    """
    Beausitful Soup web scraper designed around
    http://millercenter.org/president/speeches.
    """

    def __init__(self, *args, **kwargs):
        self.speeches = set()
        self.speech_links = self.get_speech_links()
        self.created = datetime.now()

    def __str__(self):
        return "Scraper instance {0.created}".format(self)

    def __repr__(self):
        return "Scraper instance {0.created}".format(self)

    def __len__(self):
        """Returns number of scraped speech links"""
        return len(self.speech_links)

    def get_speech_links(self):
        """Scrapes a list of links to speeches"""
        base_url = 'http://millercenter.org/president/speeches/'
        r = requests.get(base_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        little_soup = soup.find_all("a", {"href": re.compile("speeches")})
        links = {a['href'] for a in little_soup}
        return links

    def scrape(self):
        base_url = "http://millercenter.org/"
        print("Starting...")
        for slink in self.speech_links:
            url = base_url+slink
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            try:
                president = soup.article.h2.text
                little_soup = soup.find('div', {"id": "transcript"})
                speech = little_soup.text
                # import pdb; pdb.set_trace()
                title = soup.article.h1.text
                date = title.split('(')[-1].replace(')', '')
                date = datetime.strptime(date, "%B %d, %Y")

                pres, created = President.objects.get_or_create(common_name=president)
                pres.save()
                sph = Speech.objects.create(speaker=pres, body=speech, title=title,
                                            url=url, date=date)
                sph.save()
                print('saved {} - {} from {}'.format(president, title, slink))
                result = self.speeches.update((president, speech))
            except AttributeError:
                print("Skipping {url}".format(url=url))

        return result
