from django.contrib import admin

from .models import Album, Track, AlbumCover, AlbumTerms

admin.site.register((Album, Track, AlbumCover, AlbumTerms))



