from __future__ import unicode_literals

from django.db import models


class Politician(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateTimeField()
    deceased_date = models.DateTimeField(blank=True, null=True)
    years_lived = models.PositiveSmallIntegerField()


class President(Politician):
    presidecy_number = models.PositiveSmallIntegerField()
    presidency_start_year = models.DateTimeField()
    presidency_end_year = models.DateTimeField()
    ari_score = models.PositiveSmallIntegerField(blank=True, null=True)
    # TODO: wordcloud image storage ref?

    def __str__(self):
        return self.name


class Election(models.Model):
    count = models.PositiveSmallIntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    candidates = models.ManyToManyField(Politician)
    president_elect = models.ForeignKey(President)
    vice_president_elect = models.ForeignKey(Politician, blank=True, null=True)


class Speech(models.Model):
    speaker = models.ForeignKey(President, related_name='speeches')
    title = models.CharField(max_length=1024, blank=True, null=True)
    body = models.TextField()
    delivery_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} by {}'.format(self.title, self.speaker.name)
