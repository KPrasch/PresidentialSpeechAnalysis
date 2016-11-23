from .miller import MillerScraper
from profiles.models import President, Speech
import requests


m = MillerScraper()
import pdb; pdb.set_trace()
def llama():
    for pres, links in m.links.items():
        president = President.objects.create(name=pres)
        #president.save()

        for speech_link in links:
            r = requests.get(speech_link)
            import pdb; pdb.set_trace()
            s = Speech.objects.create(speaker=president)
            #s.save()
