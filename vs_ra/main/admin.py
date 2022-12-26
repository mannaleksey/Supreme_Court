from django.contrib import admin
from .models import DataCase, TextsCase, HearingCase

admin.site.register(DataCase)
admin.site.register(TextsCase)
admin.site.register(HearingCase)
