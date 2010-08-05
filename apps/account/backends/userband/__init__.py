from django.contrib.auth import authenticate, login

from registration.backends.default import DefaultBackend

from .forms import UserBandRegistrationForm

from band.models import Band, BandMember, BandRole

class UserBandBackend(DefaultBackend):
    def register(self, request, **kwargs):
        """
        Log the user even if not yet activated : prevents from waiting
        the email and loosing the will to use the website
        """
        new_user = DefaultBackend.register(self, request, **kwargs)

        # Create the band
        band_name = kwargs['band_name']
        band_slug = kwargs['band_slug']
        band_tags = kwargs['band_tags']
        band = Band.objects.create(name=band_name,
                                   slug=band_slug,
                                   genres=band_tags)

        # Add the user into the band
        user_band_roles = kwargs['user_band_roles']
        bandmember = BandMember.objects.create(band=band,
                                               user=new_user,
                                               approved=True,
                                               )

        bandmember.roles = user_band_roles
        bandmember.save()

        # authenticate() always has to be called before login(), and
        # will return the user we just created.
        new_user = authenticate(username=kwargs['username'], password=kwargs['password1'])
        login(request, new_user)

        return new_user

    def get_form_class(self, request):
        return UserBandRegistrationForm

    def post_registration_redirect(self, request, user):
        """
        After registration, redirect to the user's account page.
        """
        return ('account:registration_complete', (), {})

    def post_activation_redirect(self, request, user):
        raise NotImplementedError




