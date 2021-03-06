from django.db import models

from django.utils import timezone


class WordTag(models.Model):
    SCORE_METHODS = (('TFIDF', 'Term Frequency/Inverse Document Frequency'),
                     )

    corpus = models.ForeignKey('profiles.Speech', related_name='tagged')
    word = models.CharField(max_length=2048)
    method = models.CharField(max_length=5, choices=SCORE_METHODS)
    score = models.FloatField()
    created = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.word

    def __len__(self):
        return len(self.word)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        super().save(*args, **kwargs)
