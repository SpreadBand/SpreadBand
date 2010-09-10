from dajax.core import Dajax
from dajaxice.core import dajaxice_functions

from .forms import PressKitVideoForm
from .views import video_edit

def video_edit(request, form):
    dajax = Dajax()

    form = PressKitVideoForm(form)
    
    if form.is_valid():
        dajax.remove_css_class('#video-edit-form input', 'error')
        dajax.script("$('#video-edit-form').submit()")
    else:
        dajax.remove_css_class('#video-edit-form input', 'error')
        for error in form.errors:
            dajax.add_css_class('#id_%s' % error,'error')
            
    return dajax.json()
        
dajaxice_functions.register(video_edit)
