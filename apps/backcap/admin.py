from django.contrib import admin

from .models import Feedback, Vote

admin.site.register((Feedback, Vote))



