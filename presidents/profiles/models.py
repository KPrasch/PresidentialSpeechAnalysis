from __future__ import unicode_literals

from django.db import models


class President(models.Model):
    name = models.CharField(max_length=100)
    ari_score = models.PositiveSmallIntegerField(blank=True, null=True)
    # TODO: wordcloud image storage ref?

    def __str__(self):
        return self.name


class Speech(models.Model):
    speaker = models.ForeignKey(President, related_name='speeches')
    title = models.CharField(max_length=1024, blank=True, null=True)
    body = models.TextField()
    delivery_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} by {}'.format(self.title, self.speaker.name)
