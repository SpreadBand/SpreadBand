"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from datetime import date

import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
import django.utils.http

from guardian.shortcuts import assign
from band.models import Band, BandMember
from venue.models import Venue

from .models import GigBargain, GigBargainBand

class GigBargainFixture(object):
    def setUp(self):
        # One band, one member
        b1 = Band.objects.create(slug='band1', name='Band 1')
        u1 = User.objects.create_user('user1', 'user1@localhost', 'pass1')
        BandMember.objects.create(band=b1, user=u1)
        assign('band.can_manage', u1, b1)

        # Anoter band, another member
        b2 = Band.objects.create(slug='band2', name='Band 2')
        u2 = User.objects.create_user('user2', 'user2@localhost', 'pass2')
        BandMember.objects.create(band=b2, user=u2)
        assign('band.can_manage', u2, b2)

        # A third band, without member
        b3 = Band.objects.create(slug='band3', name='Band 3')

        # A user, with no band
        u3 = User.objects.create_user('user3', 'user3@localhost', 'pass3')

        venue = Venue.objects.create(slug='venue1', name='Venue 1')


class GigBargainAccessTestCase(GigBargainFixture, TestCase):
    def setUp(self):
        GigBargainFixture.setUp(self)

        venue = Venue.objects.get(slug='venue1')
        b1 = Band.objects.get(slug='band1')

        # create a new gigbargain
        gigbargain_date = date.today()
        gigbargain = GigBargain.objects.create(date=gigbargain_date,
                                               venue=venue,
                                               access='FREE')

        gb1 = GigBargainBand.objects.create(band=b1,
                                            bargain=gigbargain)

        self.gigbargain = gigbargain

    def test_access_anonymous(self):
        """
        Anonymous user shouldn't be able to access a bargain. They should be redirected to login URL
        """

        response = self.client.get(self.gigbargain.get_absolute_url(), follow=True)
     
        url = settings.LOGIN_URL + "/?next=" + django.utils.http.urlquote_plus(self.gigbargain.get_absolute_url())

        self.assertRedirects(response, url)


    def test_access_logged_in_notmember(self):
        """
        A user that does not belong to a band that is in a gigbargain shouldn't be able to access it
        """
        login = self.client.login(username='user3', password='pass3')
        self.assertTrue(login)

        response = self.client.get(self.gigbargain.get_absolute_url(), follow=True)
        self.failUnlessEqual(response.status_code, 403)

    def test_access_logged_in_member(self):
        """
        Member of a participating group should be able to access the bargain
        """
        login = self.client.login(username='user1', password='pass1')
        self.assertTrue(login)

        response = self.client.get(self.gigbargain.get_absolute_url(), follow=True)
        self.failUnlessEqual(response.status_code, 200)

class AbstractGigBargainStateTestCase(GigBargainFixture):
    def test_band_invitation_by_band(self):
        """
        If a band is able to invite another one
        """
        self.fail()

    def test_band_edit_mytimeline(self):
        """
        A band should be able to change its timeline.
        """
        self.fail()

    def test_band_edit_anotherbandtimeline(self):
        """
        A band should not be able to edit another band timeline
        """
        self.fail()
    

class GigBargainDraftTestCase(AbstractGigBargainStateTestCase, TestCase):
    def _login(self, username, password):
        login = self.client.login(username=username, password=password)
        self.assertTrue(login)

    def setUp(self):
        AbstractGigBargainStateTestCase.setUp(self)

        venue = Venue.objects.get(slug='venue1')
        b1 = Band.objects.get(slug='band1')

        # create a new gigbargain
        gigbargain_date = date.today()
        gigbargain = GigBargain.objects.create(date=gigbargain_date,
                                               venue=venue,
                                               state='draft',
                                               access='FREE')

        gb1 = GigBargainBand.objects.create(band=b1,
                                            bargain=gigbargain,
                                            state='negociating')

        self.gigbargain = gigbargain
    

    def test_band_invitation_by_band(self):
        self._login('user1', 'pass1')

        band2 = Band.objects.get(slug='band2')

        response = self.client.post(reverse('gigbargain:gigbargain-band-invite-band', args=[self.gigbargain.uuid]),
                                    {'band': band2.pk,
                                     'set_duration': '50 minutes'},
                                    follow=True)

        self.assertRedirects(response,
                             self.gigbargain.get_absolute_url()
                             )
        
        # Our band is part of the gigbargain and has state "invited" (= 'waiting')
        self.failUnless(band2 in self.gigbargain.bands.all())
        self.failUnlessEqual(len(GigBargainBand.objects.filter(bargain=self.gigbargain,
                                                               band=band2,
                                                               state='waiting')),
                             1)
        # We have only one more band
        self.failUnlessEqual(len(GigBargainBand.objects.filter(bargain=self.gigbargain)),
                             2)

    def test_band_edit_mytimeline(self):
        self._login('user1', 'pass1')

        band = Band.objects.get(slug='band1')

        response = self.client.post(reverse('gigbargain:gigbargain-band-edit-timeline', 
                                            args=[self.gigbargain.uuid, band.slug]
                                            ),
                                    {'band': band.pk,
                                     'starts_at': '20:00',
                                     'set_duration': '30 minutes'},
                                    follow=True)

        self.assertRedirects(response,
                             self.gigbargain.get_absolute_url()
                             )


    def test_band_edit_anotherbandtimeline(self):
        self._login('user1', 'pass1')

        another_band = Band.objects.get(slug='band2')

        response = self.client.post(reverse('gigbargain:gigbargain-band-edit-timeline', 
                                            args=[self.gigbargain.uuid, another_band.slug]
                                            ),
                                    {'band': another_band.pk,
                                     'starts_at': '20:00',
                                     'set_duration': '30 minutes'},
                                    follow=True)

        self.failUnlessEqual(response.status_code, 403)

        
        
                             
