from django.contrib import admin
from .models import WordTag

# Register your models here.
class TFIDFInline(admin.StackedInline):
    model = WordTag
    extra = 0


class WordTagAdmin(admin.ModelAdmin):
    model = WordTag
    list_display = ['word', 'score', 'corpus', ]
    list_display_links = ['word', 'score', ]



admin.site.register(WordTag, WordTagAdmin)