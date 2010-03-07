from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail
from django.forms.models import inlineformset_factory
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core import serializers
from django.db import transaction

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed

from bands.models import Band

from .models import Album, Track
from .forms import TrackForm, AlbumForm, NewTrackForm

from utils.template import direct_block_to_template

# XXX: Security
def track_new(request, band_id, album_id):
    band = get_object_or_404(Band, id=band_id)
    album = get_object_or_404(Album, id=album_id)

    # ajax ?
    if request.is_ajax():
        print "yay ajax"

    if request.method == 'POST':
        data = {'album' : album.id}
    
        track_form = NewTrackForm(data, request.FILES)
        if track_form.is_valid():
            track = track_form.save()

            # Fill the infos from the file
            from mutagen.easyid3 import EasyID3

            # XXX: make sure we don't use memory storage !
            tag = EasyID3(request.FILES['file'].temporary_file_path())
            track.title = tag['title'][0]
            
            # print "filled", track
            track.save()

            return HttpResponse(serializers.serialize('json', [track]), 
                                mimetype='text/javascript')
        else:
            return HttpResponseBadRequest()
    else:
            return HttpResponseNotAllowed(['POST'])

# XXX: Security
def track_delete(request, band_id, album_id, track_id):
    band = get_object_or_404(Band, id=band_id)
    album = get_object_or_404(Album, id=album_id)    
    track = get_object_or_404(Track, id=track_id)

    if request.is_ajax():
        track.delete()

        return HttpResponse()

    return HttpResponseBadRequest()



def album_list(request, band_id):
    """
    list all albums for the given band
    """
    band = get_object_or_404(Band, id=band_id)

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
def album_create(request, band_id):
    """
    Create a new album
    """
    band = get_object_or_404(Band, id=band_id)

    TrackInlineFormSet = inlineformset_factory(Album, Track, form=TrackForm, can_delete=False)

    if request.method == "POST":
        # Force the album's band to be us
        initial = Album(band=band)
        album_form = AlbumForm(request.POST, request.FILES, instance=initial)
        track_formset = TrackInlineFormSet(request.POST, request.FILES)

        if album_form.is_valid() and track_formset.is_valid():
            # Save the album
            album = album_form.save()

            # Save the tracks
            track_formset = TrackInlineFormSet(request.POST, request.FILES, instance=album)
            track_formset.save()
            
            # XXX: Hardcoded ! Should be 'return redirect(album)'
            #return redirect('/bands/%d/album/%d' % (band.id, album.id))
            return redirect(album)
            
    else:
        album_form = AlbumForm()
        track_formset = TrackInlineFormSet()

    return render_to_response(template_name='album/album_create.html', 
                              dictionary={'form' : album_form,
                                          'track_formset': track_formset,
                                          'band': band,
                                          },
                              context_instance=RequestContext(request),
                              )


from utils.views.jeditable import jeditable_save
# XXX: security
def album_edit_one(request, band_id, album_id):
    """
    Edit only one field of an album.
    This is usually by inline edits.
    """
    album = get_object_or_404(Album, id=album_id)
    return jeditable_save(request,
                          album,
                          AlbumForm)
    
# XXX: security
def album_edit(request, band_id, album_id):
    """
    Edit an album
    """
    band = get_object_or_404(Band, id=band_id)
    album = get_object_or_404(Album, id=album_id)

    if request.method == 'POST':
        data = request.POST.copy()
        # If we have an inline edit, use it
        if request.POST.has_key('id'):
            data.update({request.POST['id']: request.POST['value']})
            
        album_form = AlbumForm(data, instance=album)

        if album_form.is_valid():
            album_form.save()
            return HttpResponse()

def album_details(request, band_id, album_id):
    """
    Show details about an album
    """
    band = get_object_or_404(Band, id=band_id)

    return object_detail(request,
                         queryset=Album.objects.all(),
                         object_id=album_id,
                         template_object_name='album',
                         template_name='album/album_detail.html',
                         extra_context={'band': band},
                         )

