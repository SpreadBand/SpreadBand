from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.db.models import ForeignKey, PositiveIntegerField, OneToOneField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

import reversion

class Terms(models.Model):
    pass

class Contract(models.Model):
    """
    A contract between multiple parties. Can be validated only if all parties have agreed.
    """
    terms = OneToOneField(Terms,
                          help_text=_('Terms of the contract'))

    def _get_concluded(self):
        """
        Check if all parties approves this contract
        """
        ccl = True
        for party in self.parties.all():
            ccl = ccl and party.approved
        return ccl

    def _set_concluded(self, aBoolean):
        """
        Set state of all parties about conclusion
        """
        self.parties.all().update(approved=aBoolean)
    
    concluded = property(_get_concluded,
                         _set_concluded)


class Party(models.Model):
    """
    A party of a contract
    """
    contract = ForeignKey(Contract, related_name="parties")
        
    content_type = ForeignKey(ContentType, related_name="contracts")
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    approved = models.BooleanField(_('approved'), default=False, help_text=_("Designates whether the party has approved the latest revision of the contract."))


# REVERSION
reversion.register(Contract, follow=['parties', 'terms'])
reversion.register(Terms)
reversion.register(Party)
