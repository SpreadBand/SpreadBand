from django.contrib import admin

from .models import UserProfile, UserAvatar

admin.site.register((UserAvatar,))
