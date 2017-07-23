from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from profiles.models import President, Speech, Person
from . import miller_scraper
from datetime import datetime


class Command(BaseCommand):
    help = 'Downloads presidential speech corpus.'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--local',
            action='store_true',
            dest='seed',
            default=False,
            help='Use a local HTML infile of presidential speech links',
        )

        parser.add_argument(
            '--update',
            action='store_true',
            dest='update',
            default=False,
            help='Check for new changes on the remote only.',
        )

    def handle(self, *args, **options):
        if options['seed']:
            self.stdout.write(self.style.SUCCESS('Starting scraper - Load local file'))
        elif options['update']:
            self.stdout.write(self.style.SUCCESS('Starting scraper - Update live speeches'))

        start_time = datetime.now()  # Time this operation for reporting
        scraped_corpus_data = miller_scraper.scrape(seed=options['seed'])

        if options['update']:
            existing_corpus_urls = Speech.objects.values_list('url', flat=True)

            def filter_incoming_speeches(scraped, existing: list):
                difference = ((speech, s) for speech, s in scraped if speech['url'] not in existing)
                yield from difference

            incoming_corpus_data = filter_incoming_speeches(scraped_corpus_data, existing_corpus_urls)
        else:
            incoming_corpus_data = scraped_corpus_data

        duplicates = 0
        for speechdata, skipped in incoming_corpus_data:

            president, created = President.objects.get_or_create(common_name=speechdata['speaker'])
            if created:
                president.save()

            try:
                speech = Speech.objects.create(speaker=president, body=speechdata['transcript'],
                                               title=speechdata['title'], url=speechdata['url'],
                                               date=speechdata['date'])
            except IntegrityError:
                skipped += 1
                duplicates += 1
                print(f'Skip: Duplcate {speechdata["title"]}')
                continue
            else:
                self.stdout.write(self.style.SUCCESS(f'Saved speech {speech.id}'))

        """ Display Report """
        president_count = President.objects.all().count()
        speech_count = Speech.objects.all().count()

        delta = datetime.now() - start_time

        report = f'''
        Finished....................
        -----------------------------
        runtime           ......... {delta}
        new speeches      ......... {duplicates-president_count}
        
        duplicates        ......... {duplicates}
        total skipped     ......... {skipped}
        
        total presidents  ......... {president_count}
        total speeches    ......... {speech_count} 
        '''

        self.stdout.write(self.style.SUCCESS(report))
