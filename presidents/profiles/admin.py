from django.contrib import admin
from .models import President, Speech, Person

# Register your models here.
admin.site.register(President)
admin.site.register(Speech)
admin.site.register(Person)
