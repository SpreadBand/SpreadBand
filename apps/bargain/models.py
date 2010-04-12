from django.utils.translation import ugettext_lazy as _

from django.db import models
from django.db.models import ForeignKey, PositiveIntegerField, OneToOneField, ManyToManyField, BooleanField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

import reversion

class Party(models.Model):
    """
    A party of a contract
    """
    class Meta:
        verbose_name_plural = "Parties"

    content_type = ForeignKey(ContentType)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return "Party of type %s: %s" % (self.content_type,
                                         self.content_object)


class Contract(models.Model):
    """
    A contract between multiple parties. Can be validated only if all
    parties have agreed.
    """
    parties = ManyToManyField(Party, through='ContractParty', related_name='contracts')

    @property
    def is_concluded(self):
        """
        Check if all parties approves this contract
        """
        ccl = True
        for party in ContractParty.objects.filter(contract=self):
            ccl = ccl and party.approved

        return ccl

    @is_concluded.setter
    def _set_is_concluded(self, aBoolean):
        """
        Set state of all parties about conclusion
        """
        ContractParty.objects.filter(contract=self).update(approved=aBoolean)

    @models.permalink
    def get_absolute_url(self):
        return ('bargain:contract-detail', (self.id, ))

    def __unicode__(self):
        if self.is_concluded:
            concluded_str = 'concluded'
        else:
            concluded_str = 'not concluded'

        return "Contract (%s) -- %s" % (self.parties.all(),
                                        concluded_str)

class ContractParty(models.Model):
    """
    Relation between contracts and parties
    """
    class Meta:
        verbose_name_plural = "Contract parties"

    party = ForeignKey(Party)
    contract = ForeignKey(Contract)

    initiator = BooleanField(default=False, 
                             help_text=_("If the party has initiated this contract"))

    approved = models.BooleanField(_('approved'), 
                                   default=False, 
                                   help_text=_("Designates whether the party has approved the latest revision of the contract."))

    def __unicode__(self):
        return "Relation between contract '%d' and '%s'" % (self.contract_id,
                                                            self.party)
    

class Terms(models.Model):
    contract = OneToOneField(Contract, related_name='terms')

    @staticmethod
    def getForms():
        raise "Not implemented"

    def __unicode__(self):
        return "Terms for %s" % self.contract


# REVERSION
reversion.register(Contract, follow=['parties', 'terms'])
reversion.register(Terms)
reversion.register(Party)
