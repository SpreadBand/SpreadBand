from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list, object_detail
from django.forms.models import inlineformset_factory
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core import serializers
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.db import transaction

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed

from band.models import Band

from .models import Album, AlbumTrack
from .forms import TrackForm, AlbumForm, NewTrackForm, AlbumCoverForm

from utils.template import direct_block_to_template

# XXX: Security
def track_new(request, band_slug, album_slug):
    request.upload_handlers = [TemporaryFileUploadHandler()]

    band = get_object_or_404(Band, slug=band_slug)
    album = get_object_or_404(Album, slug=album_slug)

    if request.method == 'POST':
        data = {'album' : album.id}
    
        track_form = NewTrackForm(data, request.FILES)
        if track_form.is_valid():
            track = track_form.save(commit=False)
            track.album = album

            # Fill the infos from the file
            from mutagen.easyid3 import EasyID3

            # XXX: make sure we don't use memory storage !
            tag = EasyID3(request.FILES['file'].temporary_file_path())
            track.title = tag['title'][0]
            
            # print "filled", track
            track.save()

            # ajax ?
            if request.is_ajax():
                return HttpResponse(serializers.serialize('json', [track]), 
                                    mimetype='text/javascript')
            else:
                return redirect(album)

    track_form = NewTrackForm()
    return render_to_response(template_name='album/track_create.html',
                              dictionary={'track_form': track_form,
                                          'band': band},
                              context_instance=RequestContext(request)
                              )

# XXX: Security
def track_delete(request, band_slug, album_slug, track_id):
    band = get_object_or_404(Band, slug=band_slug)
    album = get_object_or_404(Album, slug=album_slug)    
    track = get_object_or_404(AlbumTrack, id=track_id)

    track.delete()

    if request.is_ajax():
        return HttpResponse()
    else:
        return redirect(album)



def album_list(request, band_slug):
    """
    list all albums for the given band
    """
    band = get_object_or_404(Band, slug=band_slug)

    if request.is_ajax():
        return direct_block_to_template(request,
                                        template='album/album_list.html',
                                        block='band_content',
                                        extra_context = {'album_list': band.albums.all}
                                        )
    else:
        return object_list(request,
                           queryset=band.albums.all(),
                           template_name='album/album_list.html',
                           template_object_name='album',
                           extra_context = {'band': band},
                           )

# XXX: security
def album_create(request, band_slug):
    """
    Create a new album
    """
    band = get_object_or_404(Band, slug=band_slug)

    TrackInlineFormSet = inlineformset_factory(Album, AlbumTrack, form=TrackForm, can_delete=False)

    if request.method == "POST":
        # Force the album's band to be us
        initial = Album(band=band)
        album_form = AlbumForm(request.POST, request.FILES, instance=initial)

        if album_form.is_valid():
            # Save the album
            album = album_form.save()
            
            return redirect(album)
            
    else:
        album_form = AlbumForm()

    return render_to_response(template_name='album/album_create.html', 
                              dictionary={'form' : album_form,
                                          'band': band,
                                          },
                              context_instance=RequestContext(request),
                              )


from utils.views.jeditable import jeditable_save
# XXX: security
def album_edit_one(request, band_slug, album_slug):
    """
    Edit only one field of an album.
    This is usually by inline edits.
    """
    album = get_object_or_404(Album, id=album_slug)
    return jeditable_save(request,
                          album,
                          AlbumForm)
    
# XXX: security
def album_edit(request, band_slug, album_slug):
    """
    Edit an album
    """
    band = get_object_or_404(Band, slug=band_slug)
    return update_object(request,
                         Album,
                         slug=album_slug,
                         template_name='album/album_edit.html',
                         extra_context={'band': band})

def album_details(request, band_slug, album_slug):
    """
    Show details about an album
    """
    band = get_object_or_404(Band, slug=band_slug)

    return object_detail(request,
                         queryset=Album.objects.all(),
                         slug=album_slug,
                         template_object_name='album',
                         template_name='album/album_detail.html',
                         extra_context={'band': band},
                         )

def cover_new(request, band_slug, album_slug):
    band = get_object_or_404(Band, slug=band_slug)
    album = get_object_or_404(Album, slug=album_slug)

    if request.method == 'POST':
        cover_form = AlbumCoverForm(request.POST, request.FILES)

        if cover_form.is_valid():
            cover = cover_form.save(commit=False)
            cover.album = album

            cover.save()

            return redirect(album)
    else:
        cover_form = AlbumCoverForm()

    return render_to_response(template_name='album/albumcover_new.html',
                              dictionary={'form': cover_form,
                                          'band': band
                                          },
                              context_instance=RequestContext(request),
                              )
