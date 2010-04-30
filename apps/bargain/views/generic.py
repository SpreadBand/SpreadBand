from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.template import RequestContext

from ..models import Contract, Party, ContractParty
from ..signals import contract_concluded, contract_new_init

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
    

from django.forms.models import inlineformset_factory, modelformset_factory, formset_factory

def contract_new(request, aTermsClass, initial=None, formset_initial=None, extra_context={}, next=None):
    terms_form_class, formset_class = aTermsClass.getForm()

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
                    # XXX: hardcoded
                    model.bargain = terms
                    model.save()

            # FIXME: Not sure if we need that, but it seems to...
            terms_form.save_m2m()

            # Create the parties and link them
            # First one is considered to be the initiator
            for i, participant in enum(terms.getParticipants()):
                get_or_create_party(participant, contract, is_initiator=(i==0))

            return redirect('bargain:contract-detail', contract.id)

    terms_form = terms_form_class(request.POST or None, request.FILES or None, initial=initial)
    formset = formset_class(request.POST or None, request.FILES or None, initial=formset_initial)

    # Send the "contract new init" callback
    # contract_new_init.send(terms_form)

    return render_to_response(template_name='bargain/%s_new.html' % aTermsClass.__name__.lower(),
                              dictionary={'form': terms_form,
                                          'formset': formset},
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )

from django.contrib.contenttypes.models import ContentType

from ..signals import contract_concluded

def contract_approve(request, contract_id, aTermClass, participant):
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

    # Set to approved
    contractparty.approved = True
    contractparty.save()

    # Check if this contract is concluded. If so, trigger the signal
    if contract.is_concluded:
        contract_concluded.send(sender=aTermClass, aContract=contract)

    return redirect(contract)

def contract_disapprove(request, contract_id, aTermClass, participant):
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

    # Set to disapproved
    contractparty.approved = False
    contractparty.save()

    return redirect(contract)



def contract_update(request, contract_id, aTermClass, participant):
    """
    Updating a contract means altering its terms. When one party
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
    terms_form_class, formset_class = aTermClass.getForm()

    terms_form = terms_form_class(request.POST or None, request.FILES or None,
                                  instance=terms)
    terms_formset = formset_class(request.POST or None, request.FILES or None,
                                  instance=terms)

    if request.method == 'POST':
        if terms_form.is_valid() and terms_formset.is_valid():
            # Unvalidate contract for every party except the participant
            ContractParty.objects.filter(contract=contract).exclude(party=party).update(approved=False)
            ContractParty.objects.filter(contract=contract, party=party).update(approved=True)

            # Save the terms
            terms = terms_form.save()
            terms_formset.save()

            return redirect(contract)

    return render_to_response(template_name='bargain/contract_update.html',
                              dictionary={'contract': contract,
                                          'terms': terms,
                                          'terms_form': terms_form,
                                          'terms_formset': terms_formset},
                              )
                              

def contract_detail(request, contract_id, subtemplate_name):
    contract = get_object_or_404(Contract, id=contract_id)

    contract_parties = ContractParty.objects.filter(contract=contract)
    
    return object_detail(request,
                         queryset=Contract.objects.all(),
                         object_id=contract_id,
                         template_object_name='contract',
                         template_name='bargain/contract_detail.html',
                         extra_context={'contract_parties': contract_parties,
                                        'subtemplate_name': subtemplate_name},
                         )
