from django.contrib.contenttypes.models import ContentType
from django.forms.models import inlineformset_factory, modelformset_factory, formset_factory
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail

from ..models import Contract, Party, ContractParty

from ..signals import contract_new as signal_contract_new
from ..signals import contract_concluded as signal_contract_concluded
from ..signals import contract_approved as signal_contract_approved
from ..signals import contract_disapproved as signal_contract_disapproved
from ..signals import contract_amended as signal_contract_amended

def contract_list(request, queryset=Contract.objects.all()):
    return object_list(request,
                       queryset=queryset,
                       template_name='bargain/contract_list.html',
                       template_object_name='contract',
                       )

def get_or_create_party(aModel, aContract, is_initiator=False):
    party_type = ContentType.objects.get_for_model(aModel)

    try:
        party = Party.objects.get(content_type__pk=party_type.id,
                                  object_id=aModel.id)
    except Party.DoesNotExist:
        party = Party.objects.create(content_object=aModel)

    finally:
        return ContractParty.objects.create(contract=aContract,
                                            initiator=is_initiator,
                                            approved=is_initiator,
                                            party=party)
    



def contract_new(request, aTermsClass, initial=None, formset_initial=None, extra_context={}, post_create_redirect=None):
    terms_form_class, inline_formset = aTermsClass.getForm()
    formset_fk = inline_formset[0]
    formset_class = inline_formset[1]

    if request.method == 'POST':
        terms_form = terms_form_class(request.POST, request.FILES)
        formset = formset_class(request.POST, request.FILES)

        if terms_form.is_valid() and formset.is_valid():
            terms = terms_form.save(commit=False)

            # Create the contract and set it
            contract = Contract.objects.create()

            terms.contract = contract
            terms.save()

            # Renew the formset by binding it to our terms
            for i in range(0, formset.total_form_count()):
                form = formset.forms[i]
                if form.is_valid():
                    model = form.save(commit=False)
                    setattr(model, formset_fk, terms)
                    model.save()

            # FIXME: Not sure if we need that, but it seems to...
            terms_form.save_m2m()

            # Create the parties and link them
            # First one is considered to be the initiator
            for i, participant in enumerate(terms.getParticipants()):
                get_or_create_party(participant, contract, is_initiator=(i==0))

            # Send the "contract new init" callback
            signal_contract_new.send(sender=aTermsClass, aContract=contract)

            # Compute the redirect page
            return redirect(post_create_redirect or 'bargain:contract-detail',
                            contract.id)

    terms_form = terms_form_class(request.POST or None, request.FILES or None, initial=initial)
    formset = formset_class(request.POST or None, request.FILES or None, initial=formset_initial)

    return render_to_response(template_name='bargain/%s_new.html' % aTermsClass.__name__.lower(),
                              dictionary={'form': terms_form,
                                          'formset': formset},
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )

def contract_approve(request, contract_id, aTermClass, participant, post_approve_redirect):
    """
    Approving a contract means a party agrees to the current terms.
    """
    participant_type = ContentType.objects.get_for_model(participant)

    contract = get_object_or_404(Contract,
                                 pk=contract_id)

    party = get_object_or_404(Party,
                              content_type__pk=participant_type.id,
                              object_id=participant.id)
    
    contractparty = get_object_or_404(ContractParty,
                                      contract=contract,
                                      party=party)

    # Don't do anything if we had already approved it
    if not contractparty.approved:
        contractparty.approved = True
        contractparty.save()

        # Send signal
        signal_contract_approved.send(sender=aTermClass, aContract=contract, aParticipant=participant)

        # Check if this contract is concluded. If so, trigger the signal
        if contract.is_concluded:
            signal_contract_concluded.send(sender=aTermClass, aContract=contract, aUser=request.user)

    return redirect(post_approve_redirect, contract.id)

def contract_disapprove(request, contract_id, aTermClass, participant, post_disapprove_redirect):
    """
    Disapproving a contract means a party disaagrees to the current terms.
    """
    participant_type = ContentType.objects.get_for_model(participant)

    contract = get_object_or_404(Contract,
                                 pk=contract_id)

    party = get_object_or_404(Party,
                              content_type__pk=participant_type.id,
                              object_id=participant.id)
    
    contractparty = get_object_or_404(ContractParty,
                                      contract=contract,
                                      party=party)

    # Don't do anything if already disapproved
    if contractparty.approved:
        # Set to disapproved
        contractparty.approved = False
        contractparty.save()

        # Send signal
        signal_contract_disapproved.send(sender=aTermClass, aContract=contract, aParticipant=participant)

    return redirect(post_disapprove_redirect, contract.id)



def contract_update(request, contract_id, aTermClass, participant, post_update_redirect):
    """
    Updating a contract means amending its terms. When one party
    performs this action, all other parties gets their approval
    resetted to false.
    """
    # Look up needed objects
    contract = get_object_or_404(Contract, pk=contract_id)
    terms = get_object_or_404(aTermClass, contract=contract)

    participant_type = ContentType.objects.get_for_model(participant)
    party = get_object_or_404(Party,
                              content_type__pk=participant_type.id,
                              object_id=participant.id)

    # Get the form from the model
    terms_form_class, inline_formset_class = aTermClass.getForm()

    terms_form = terms_form_class(request.POST or None, request.FILES or None,
                                  instance=terms)

    # Rebuild the formset using a modelformset from the model given by
    # the modelformset (total crap, but don't know how to do better)
    inline_model = inline_formset_class[1].form.Meta.model
    inline_modelformset_class = modelformset_factory(inline_model, 
                                                     exclude=getattr(inline_formset_class[1].form.Meta, 'exclude', None),
                                                     fields=getattr(inline_formset_class[1].form.Meta, 'fields', None),
                                                     extra=0)
                                                     


    if request.method == 'POST':
        terms_formset = inline_modelformset_class(request.POST, request.FILES or None)

        if terms_form.is_valid() and terms_formset.is_valid():
            # Unvalidate contract for every party except the participant
            ContractParty.objects.filter(contract=contract).exclude(party=party).update(approved=False)
            ContractParty.objects.filter(contract=contract, party=party).update(approved=True)

            # Save the terms
            terms = terms_form.save()
            terms_formset.save()

            # Send signal
            signal_contract_amended.send(sender=aTermClass, aContract=contract, aParticipant=participant)

            return redirect(post_update_redirect, (contract.id))
    else:
        terms_formset = inline_modelformset_class(queryset=inline_model.objects.filter(bargain__id=contract_id))

    return render_to_response(template_name='bargain/%s_update.html' % aTermClass.__name__.lower(),
                              dictionary={'contract': contract,
                                          'terms': terms,
                                          'terms_form': terms_form,
                                          'terms_formset': terms_formset},
                              context_instance=RequestContext(request)
                              )
                              

def contract_detail(request, contract_id, aTermClass, extra_context={}):
    contract = get_object_or_404(Contract, id=contract_id)

    contract_parties = ContractParty.objects.filter(contract=contract)

    extra_context.update({'contract': contract,
                          'contract_parties': contract_parties})

    return render_to_response(template_name='bargain/%s_detail.html' % aTermClass.__name__.lower(),
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )
