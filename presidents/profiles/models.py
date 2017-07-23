from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils.text import slugify
from readability.ari import ari_score
from tf_idf.main import score_corpus
from language.models import WordTag


class Person(models.Model):
    first_name = models.CharField(max_length=500, blank=True, null=True)
    middle_name = models.CharField(max_length=500, blank=True, null=True)
    last_name = models.CharField(max_length=500, blank=True, null=True)
    slug = models.SlugField(null=True, blank=True, editable=False)
    common_name = models.CharField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=500, blank=True, null=True)  # Keep as CharField
    birth_location = models.CharField(max_length=1024, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    deceased_date = models.DateField(blank=True, null=True)
    death_location = models.CharField(max_length=1024, blank=True, null=True)
    education = models.CharField(max_length=1024, blank=True, null=True)
    lifespan = models.PositiveSmallIntegerField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True, editable=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        """
        Assures that each Person's full name is unique. There can only be one!
        """
        unique_together = ('first_name', 'middle_name', 'last_name')
        # sets the plural of person to people
        verbose_name_plural = 'people'
        # describe how you want this to be ordered in the database
        ordering = ['-birth_date']  # order by reverse birth dates

    def save(self, *args, **kwargs):
        self.slug = slugify(self.common_name)
        self.set_age()
        super().save(*args, **kwargs)

    def __str__(self):
        names = " ".join([self.first_name, self.middle_name, self.last_name])
        return names

    def set_age(self):
        """
        Calculates and returns either the age or the years lived of the person
        """
        if self.birth_date and self.deceased_date:
            # gets the difference as a timedelta objects
            delta = self.deceased_date - self.birth_date
            # gets the days of the timedelta and converts to years
            self.lifespan = delta.days // 365

        if self.birth_date:
            delta = datetime.datetime.now().date() - self.birth_date
            self.age = delta.days // 365


class President(Person):
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
    presidency_number = models.PositiveSmallIntegerField(blank=True, null=True)
    party = models.CharField(max_length=200, blank=True, null=True)
    start_year = models.DateTimeField(blank=True, null=True)
    end_year = models.DateTimeField(blank=True, null=True)
    reason_left_office = models.CharField(max_length=3, choices=REASONS, blank=True, null=True)
    # wordcloud = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.common_name


class Speech(models.Model):
    speaker = models.ForeignKey(President, related_name='speeches')
    title = models.CharField(max_length=1024, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=1024, blank=True, null=True, editable=False)
    body = models.TextField()
    url = models.URLField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    ARI_score = models.PositiveSmallIntegerField(default=0, editable=False)
    ARI_display = models.CharField(max_length=100, default="Not Scored Yet.", editable=False)

    class Meta:
        unique_together = ['speaker', 'title', 'date']
        ordering = ['-date', 'speaker']

    def save(self, refresh=True, *args, **kwargs):

        self.slug = slugify(self.title)

        if refresh:
            score, scoredata = ari_score(self.body)
            self.ARI_score = score
            self.ARI_display = scoredata['grade_level']

        super().save(*args, **kwargs)

    def tfidf(self, everybody=False):
        if everybody:
            all_speeches_corpus = Speech.objects.all().values_list('body', flat=True)
            corpus = all_speeches_corpus
        else:
            presidential_corpus = self.speaker.speeches.all().values_list('body', flat=True)
            corpus = presidential_corpus

        speech = self.body
        word_scores = score_corpus(speech, corpus)

        for word, score in word_scores:
            tag, created = WordTag.objects.get_or_update(speech=self, word=word, score=score)
            tag.save()
        return word_scores

    def __str__(self):
        return '{} by {}'.format(self.title, self.speaker.common_name)

    def __len__(self):
        return len(self.body)

