from django.contrib.auth.models import User
from django.test import TestCase

from reversion import revision
from reversion.models import Version

from .models import Terms, Contract, Party

class ContractTest(TestCase):
    def setUp(self):
        terms = Terms()
        terms.save()
        self.c = Contract(terms=terms)
        self.c.save()

        user = User(pk=1)    
        p = Party(contract=self.c, content_object=user)
        p.save()


    def testConcluded(self):
        """
        Test the dynamic concluded field
        """
        self.assertEqual(self.c.concluded, False)

        self.c.concluded = True
        self.assertEqual(self.c.concluded, True)

        self.c.parties.all().delete()
        self.assertEqual(self.c.concluded, True)

    def testVersions(self):
        """
        Test the versioning mechanism
        """
        @revision.create_on_success
        def make_changes(bool):
            self.c.parties.all().update(approved=bool)
            self.c.save()

        make_changes(False)
        make_changes(True)
        
        versions = Version.objects.get_for_object(self.c)
        self.assertEqual(len(versions), 2)
        self.assertEqual(len(versions[0].revision.version_set.all()), 3)

        print self.c.parties.all()[0].approved

        old_contract = versions[0].get_object_version()

        old_party = versions[1].revision.version_set.all()[2]

        #print old_party.field_dict

        old_contract = versions[0].object_version

        
        


        
