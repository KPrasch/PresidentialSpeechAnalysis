from __future__ import unicode_literals
from django.db import models
import datetime


class Person(models.Model):
    first_name = models.CharField(max_length=500, blank=True, null=True)
    middle_name = models.CharField(max_length=500, blank=True, null=True)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=500, blank=True, null=True) # Keep as CharField
    birth_location = models.CharField(max_length=1024, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    deceased_date = models.DateField(blank=True, null=True)
    death_location = models.CharField(max_length=1024, blank=True, null=True)
    education = models.CharField(max_length=1024, blank=True, null=True)
    years_lived = models.PositiveSmallIntegerField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        """
        Assures that each Person's full name is unique. There can only be one!
        """
        unique_together = ('first_name', 'middle_name', 'last_name')
        # sets the plural of person to people
        verbose_name_plural = 'people'
        # describe how you want this to be ordered in the database
        ordering = ['-birth_date'] # order by reverse birth dates

    def save(self, *args, **kwargs):
        self.calc_years_lived_or_age()
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        names = " ".join([self.first_name, self.middle_name, self.last_name])
        return names

    def calc_years_lived_or_age(self):
        '''
        Calculates and returns either the age or the years lived of the person
        '''
        if self.deceased_date != None:
            # gets the difference as a timedelta objects
            delta = self.deceased_date - self.birth_date
            # gets the days of the timedelta and converts to years
            self.years_lived = delta.days // 365
        else:
            delta = datetime.datetime.now().day - self.birth_date
            self.age = delta.days // 365



class Politician(Person):
    political_party = models.CharField(max_length=100, blank=True, null=True)



class President(Politician):
    REASONS = (
    ('NSR', 'Did Not Seek Re-election'),
    ('TME', 'Term Ended'),
    ('LRE', 'Lost'),
    ('DIO', 'Died in Office'),
    ('ASN', 'Assasinated'),
    ('RSG', 'Resigned'),
    ('IPH', 'Impeached'),
    )
    elections_won = models.PositiveSmallIntegerField(default=0)
    presidecy_number = models.PositiveSmallIntegerField()
    start_year = models.DateTimeField()
    end_year = models.DateTimeField()
    reason_left_office = models.CharField(max_length=3, choices=REASONS)
    ari_score = models.PositiveSmallIntegerField(blank=True, null=True)
    wordcloud = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Election(models.Model):
    count = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    candidates = models.ManyToManyField(Politician)
    president_elect = models.ForeignKey(President, related_name='election')
    vice_president_elect = models.ForeignKey(Politician, related_name='election_as_vp', blank=True, null=True)

    def __str__(self):
        return 'Election #: {}, {}'.format(self.count, self.start_date)


class Speech(models.Model):
    speaker = models.ForeignKey(President, related_name='speeches')
    title = models.CharField(max_length=1024, blank=True, null=True)
    body = models.TextField()
    delivery_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} by {}'.format(self.title, self.speaker.name)
