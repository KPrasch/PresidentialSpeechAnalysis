from django.core.management.base import BaseCommand, CommandError
from profiles.models import President, Speech, Person
from . import miller_scraper


class Command(BaseCommand):
    help = 'Downloads presidential speech corpus.'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting scraper'))

        links = miller_scraper.get_speech_links(seed=True)
        presidential_speech_corpus = miller_scraper.scrape(links)

        for president_name, speeches in presidential_speech_corpus.items():
            president, created = President.objects.get_or_create(common_name=speeches[0]['name'])
            president.save()

            for speechdata in speeches:
                speech = Speech.objects.create(speaker=president, body=speechdata['transcript'],
                                               title=speechdata['title'], url=speechdata['url'],
                                               date=speechdata['date'])
                speech.save()
                self.stdout.write(self.style.SUCCESS(f'Saves speech {speech.id}'))
