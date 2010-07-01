from django.contrib.auth.models import User
from django.test import TestCase

from reversion import revision
from reversion.models import Version

from .models import Terms, Contract, Party, ContractParty

class ContractTest(TestCase):
    def setUp(self):
        self.c = Contract()
        self.c.save()

        terms = Terms(contract=self.c)
        terms.save()

        user = User(id=1)
        p = Party(content_object=user)
        p.save()

        cp = ContractParty(party=p, contract=self.c)
        cp.save()

    def testConcludedOne(self):
        """
        Test the dynamic concluded field
        """
        # test with one user
        self.assertEqual(self.c.is_concluded, False)

        self.c.is_concluded = True
        self.assertEqual(self.c.is_concluded, True)

        self.c.parties.all().delete()
        self.assertEqual(self.c.is_concluded, False)

    def testConcludedMultiple(self):
        """
        Test with 2 bargainers
        """
        # Create a second user
        user2 = User(id=2)
        p2 = Party(content_object=user2)
        p2.save()

        cp2 = ContractParty(party=p2, contract=self.c)
        cp2.save()

        self.assertEqual(self.c.is_concluded, False)

        self.c.is_concluded = True
        self.assertEqual(self.c.is_concluded, True)

        cp2.approved = False
        cp2.save()

        self.assertEqual(self.c.is_concluded, False)

        cp2.approved = True
        cp2.save()

        self.assertEqual(self.c.is_concluded, True)

