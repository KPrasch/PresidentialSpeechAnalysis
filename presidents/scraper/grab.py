from .miller import PresidentSpeechLinkScraper
from profiles.models import President, Speech
from bs4 import BeautifulSoup
import requests


m = PresidentSpeechLinkScraper()

def get_data():
    for name, links in m.speeches.items():
        president = President.objects.create(miller_name=name)
        #president.save()

        for speech_link in links:
            r = requests.get(speech_link)
            soup = BeautifulSoup(r.text, 'html.parser')
            transcript = soup.find("div", {"id": "transcript"})
            clean = transcript.text.replace('\n', '')
            import pdb; pdb.set_trace()

            s = Speech.objects.create(speaker=president)
            #s.save()
