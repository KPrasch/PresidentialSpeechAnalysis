from django.contrib import admin
from .models import Election, President, Speech, Politician

# Register your models here.
admin.site.register(President)
admin.site.register(Politician)
admin.site.register(Speech)
admin.site.register(Election)
