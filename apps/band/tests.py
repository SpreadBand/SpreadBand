from django.test import TestCase

from .models import Band

class BandTest(TestCase):
    def setUp(self):
        self.b = Band(name='Anathema',
                      style_tags='doom metal',
                      biography='awesome to loosesome',
                      founded_on='1990-03-16'
                      )
                      
        self.b.save()
        
    def testVisibility(self):
        pass

