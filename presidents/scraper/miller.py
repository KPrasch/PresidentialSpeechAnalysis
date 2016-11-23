from bs4 import BeautifulSoup
import requests


class MillerScraper:
    base_url = 'http://millercenter.org/president/'

    def __init__(self, *args, **kwargs):
        self.links = self.make_real_links()
        super(MillerScraper, self).__init__(*args, **kwargs)

    def __len__(self):
        return len(self.links)

    def parse_president_speeches(self, president):
        r = requests.get('{}{}'.format(self.base_url, president))
        soup = BeautifulSoup(r.text, 'html.parser')
        speeches_soup = soup.find("div", {"id": "speeches"})
        return speeches_soup

    @staticmethod
    def compile_speech_links(speeches_soup):
        def get_speech_link(l):
            l = l.a.attrs['href']
            return l
        return [get_speech_link(s) for s in speeches_soup.find_all('span')]

    def scrape_president_speech_links(self, president='washington'):
        speeches_soup = self.parse_president_speeches(president)
        links = self.compile_speech_links(speeches_soup)
        return links

    @staticmethod
    def get_presidents_list():
        r = requests.get('http://millercenter.org/president')
        soup = BeautifulSoup(r.text, 'html.parser')
        speeches_soup = soup.find("div", {"id": "presidents-list"})
        speeches_soup = speeches_soup.find_all('h2')
        return [p.text for p in speeches_soup]

    def make_real_links(self):
        plist = self.get_presidents_list()

        plist[40] = 'George H.W. Bush'  # 'George H.\xa0W. Bush'
        plist[7] = 'vanburen' # buren > vanburen
        clean_plist = [fn.split()[-1].strip().lower() for fn in plist]

        result = {pres: [self.base_url+l for l in self.scrape_president_speech_links(president=pres)] \
                                for pres in clean_plist }


        return result
