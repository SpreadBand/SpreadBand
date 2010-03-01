from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail
from django.forms.models import inlineformset_factory

from django.db import transaction

from django.shortcuts import render_to_response, get_object_or_404, redirect

from bands.models import Band

from .models import Album, Track
from .forms import TrackForm, AlbumForm

def album_list(request, band_id):
    """
    list all albums for the given band
    """
    band = get_object_or_404(Band, id=band_id)

    return object_list(request,
                       queryset=band.albums.all(),
                       template_name='album/album_list.html',
                       template_object_name='album',
                       )


def album_create(request, band_id):
    """
    Create a new album
    """
    band = get_object_or_404(Band, id=band_id)

    TrackInlineFormSet = inlineformset_factory(Album, Track, form=TrackForm, can_delete=False)

    if request.method == "POST":
        # Force the album's band to be us
        initial = Album(band=band)
        album_form = AlbumForm(request.POST, instance=initial)
        track_formset = TrackInlineFormSet(request.POST, request.FILES)

        if album_form.is_valid() and track_formset.is_valid():
            # Save the album
            album = album_form.save()

            # Save the tracks
            track_formset = TrackInlineFormSet(request.POST, request.FILES, instance=album)
            track_formset.save()
            
            # XXX: Hardcoded ! Should be 'return redirect(album)'
            return redirect('/bands/%d/album/%d' % (band.id, album.id))
            
    else:
        album_form = AlbumForm()
        track_formset = TrackInlineFormSet()

    return render_to_response("album/album_create.html", {
            "form" : album_form,
            "track_formset": track_formset,
            })


def album_details(request, band_id, album_id):
    """
    Show details about an album
    """
    return object_detail(request,
                         queryset=Album.objects.all(),
                         object_id=album_id,
                         template_object_name='album',
                         template_name='album/album_detail.html',
                         )

