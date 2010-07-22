import django.http
import django.template
import django.template.loader

class Django403Middleware(object):
    """
    Replaces vanilla django.http.HttpResponseForbidden() responses
    with a rendering of 403.html
    """
    def process_response(self, request, response):
        # If the response object is a vanilla 403 constructed with
        # django.http.HttpResponseForbidden() then call our custom 403 view
        # function
        if isinstance(response, django.http.HttpResponseForbidden) and \
                set(dir(response)) == set(dir(django.http.HttpResponseForbidden())):

            t = django.template.loader.get_template('403.html')
            template_values = {}
            template_values['request'] = request

            return django.http.HttpResponseForbidden(t.render(django.template.RequestContext(request, template_values)))

        return response







