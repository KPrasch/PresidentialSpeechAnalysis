from bs4 import BeautifulSoup
import requests


class PresidentSpeechLinkScraper:
    base_url = 'http://millercenter.org/president/speeches'
    transcript_base = 'http://millercenter.org'

    def __init__(self, *args, **kwargs):
        self.speeches = self.parse()

    def __len__(self):
        return len(self.speeches.keys())

    def parse(self):
        r = requests.get(self.base_url)
        soup = BeautifulSoup(r.text, 'html.parser')

        codex = dict()
        pres_soup = soup.find_all("a", {"class": "transcript"})

        for a in pres_soup:
            url = a['href']
            last_name = url.split('/')[2]
            try:
                codex[last_name].append(self.transcript_base+url)
            except KeyError:
                codex[last_name] = [self.transcript_base+url]

        return codex

        
