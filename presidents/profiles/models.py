from __future__ import unicode_literals
from django.db import models
import datetime


class Politician(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    deceased_date = models.DateField(blank=True, null=True)
    political_party = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)

    def calc_years_lived_or_age(self):
        '''
        Calculates and returns either the age or the years lived of the politician
        '''
        if self.deceased_date != None:
            # gets the difference as a timedelta objects
            delta = self.deceased_date - self.birth_date
            # gets the days of the timedelta and converts to years
            years_lived = delta.days // 365
            return years_lived
        else:
            delta = datetime.datetime.now().day - self.birth_date
            age = delta.days // 365
            return age
    # property() is used to create these attributes only made from methods
    years_lived = property(calc_years_lived_or_age)
    age = property(calc_years_lived_or_age)


class President(Politician):
    presidecy_number = models.PositiveSmallIntegerField()
    presidency_start_year = models.DateTimeField()
    presidency_end_year = models.DateTimeField()
    ari_score = models.PositiveSmallIntegerField(blank=True, null=True)
    wordcloud = models.ImageField()
    # TODO: wordcloud image storage ref?

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
