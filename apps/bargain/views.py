from django.views.generic.create_update import create_object
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext

from .models import Contract, Party, ContractParty

def contract_list(request, queryset=Contract.objects.all()):
    return object_list(request,
                       queryset=queryset,
                       template_name='bargain/contract_list.html',
                       template_object_name='contract',
                       )

def contract_new(request, aTermsClass, participants=[], model_before_save_cb=None, extra_context={}):
    terms_form_class = aTermsClass.getForm()

    if request.POST:
        terms_form = terms_form_class(request.POST)
        if terms_form.is_valid():
            terms = terms_form.save(commit=False)

            # Create the contract and set it
            contract = Contract.objects.create()

            terms.contract = contract

            # Call the before save callback if needed
            if model_before_save_cb:
                model_before_save_cb(request, terms)

            terms.save()


            # Create the parties and link them
            from django.contrib.contenttypes.models import ContentType
            initiator_type = ContentType.objects.get_for_model(request.user)

            try:
                initiator = Party.objects.get(content_type__pk=initiator_type.id,
                                              object_id=request.user.id)
            except Party.DoesNotExist:
                initiator = Party.objects.create(content_object=request.user)

            finally:
                ContractParty.objects.create(contract=contract,
                                             initiator=True,
                                             approved=True,
                                             party=initiator)
            
            # For each participant, look up its party object and link
            # it to this contract
            for participant in participants:
                participant_type = ContentType.objects.get_for_model(participant)

                try:
                    party = Party.objects.get(content_type__pk=participant_type.id,
                                              object_id=participant.id)
                except Party.DoesNotExist:
                    party = Party.objects.create(content_object=participant)

                finally:
                    ContractParty.objects.create(contract=contract,
                                                 party=party)

            return redirect('bargain:contract-list')

    else:
        terms_form = terms_form_class()

    return render_to_response(template_name='bargain/contract_new.html',
                              dictionary={'form': terms_form},
                              context_instance=RequestContext(request,
                                                              extra_context),
                              )

from django.contrib.contenttypes.models import ContentType

from .signals import contract_concluded

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
    resetted.
    """
    # Look up needed objects
    contract = get_object_or_404(Contract, pk=contract_id)
    terms = get_object_or_404(aTermClass, contract=contract)

    participant_type = ContentType.objects.get_for_model(participant)
    party = get_object_or_404(Party,
                              content_type__pk=participant_type.id,
                              object_id=participant.id)

    # Get the form from the model
    terms_form_class = aTermClass.getForm()

    if request.method == 'POST':
        terms_form = terms_form_class(request.POST, request.FILES,
                                      instance=terms)

        if terms_form.is_valid():
            # Unvalidate contract for every party except the participant
            ContractParty.objects.filter(contract=contract).exclude(party=party).update(approved=False)
            ContractParty.objects.filter(contract=contract, party=party).update(approved=True)

            # Save the terms
            terms = terms_form.save()

            return redirect(contract)
    else:
        terms_form = terms_form_class(instance=terms)

    return render_to_response(template_name='bargain/contract_update.html',
                              dictionary={'contract': contract,
                                          'terms': terms,
                                          'terms_form': terms_form},
                              )
                              

def contract_detail(request, contract_id):
    contract = get_object_or_404(Contract, id=contract_id)

    contract_parties = ContractParty.objects.filter(contract=contract)
    
    return object_detail(request,
                         queryset=Contract.objects.all(),
                         object_id=contract_id,
                         template_object_name='contract',
                         template_name='bargain/contract_detail.html',
                         extra_context={'contract_parties': contract_parties},
                         )
