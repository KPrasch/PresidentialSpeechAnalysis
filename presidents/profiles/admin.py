from django.contrib import admin
from .models import President, Speech, Person


class SpeechInline(admin.TabularInline):
    model = Speech


class PresidentAdmin(admin.ModelAdmin):
    inlines = [SpeechInline, ]
    list_display_links = ['common_name', 'presidency_number']
    list_display = ('presidency_number', 'common_name',
                    'start_year', 'end_year',
                    'first_name', 'middle_name', 'last_name',
                    )


admin.site.register(President, PresidentAdmin)
admin.site.register(Speech)
admin.site.register(Person)
