from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.utils.html import strip_tags
from django.forms import model_to_dict

def jeditable_save(request, anInstance, aFormClass):
    """
    Update only one field of a model.
    """
    if request.method == 'POST':
        # First, get the data back from the model and alter it with our new value
        data = model_to_dict(anInstance)
        data.update({request.POST['id']: strip_tags(request.POST['value'])})

        # Create a form, and feed it
        form = aFormClass(data, instance=anInstance)

        # Make sure we're trying to update a field that is allowed in the form
        if not form.fields.has_key(request.POST['id']):
            return HttpResponseBadRequest()

        if form.is_valid():
            model = form.save()
            # Return the new value of our updated field
            return HttpResponse(form.cleaned_data[request.POST['id']], mimetype="text/plain")
        else:
            return HttpResponseBadRequest()
    else:
        # We only allow POST method
        return HttpResponseNotAllowed(['POST'])
    


