from bs4 import BeautifulSoup
import requests


class PresidentSpeechLinkScraper:
    base_url = 'http://millercenter.org/president/speeches'
    transcript_base = 'http://millercenter.org'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    def __init__(self, *args, **kwargs):
        self.speeches = self.parse()

    def __len__(self):
        return len(self.speeches.keys())

    def get_presidents_list(self):
        little_soup = self.soup.find_all("h2", {"class": "president"})
        import pdb; pdb.set_trace()
        presies = [s.content[2] for s in little_soup]
        return presies

    def parse(self):
        codex = dict()
        pres_soup = self.soup.find_all("a", {"class": "transcript"})

        for a in pres_soup:
            url = a['href']
            last_name = url.split('/')[2]
            try:
                codex[last_name].append(self.transcript_base+url)
            except KeyError:
                codex[last_name] = [self.transcript_base+url]

        return codex
