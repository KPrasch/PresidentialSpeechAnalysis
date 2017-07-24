from django.contrib import admin
from .models import President, Speech, SpeechSimilarity
from language.admin import TFIDFInline



class SpeechInline(admin.TabularInline):
    model = Speech
    extra = 0


class SpeechAdmin(admin.ModelAdmin):
    inlines = [TFIDFInline, ]
    readonly_fields = ['ARI_score', 'ARI_display', 'body', 'summary']


class PresidentAdmin(admin.ModelAdmin):
    inlines = [SpeechInline, ]
    list_display_links = ['common_name', 'presidency_number']
    list_display = ('presidency_number', 'common_name',
                    'start_year', 'end_year',
                    'first_name', 'middle_name', 'last_name',
                    )

class SpeechSimilarityAdmin(admin.ModelAdmin):
    readonly_fields = ['score', 'target', 'source']


admin.site.register(President, PresidentAdmin)
admin.site.register(Speech, SpeechAdmin)
admin.site.register(SpeechSimilarity, SpeechSimilarityAdmin)
