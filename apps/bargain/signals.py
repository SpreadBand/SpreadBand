import django.dispatch

contract_concluded = django.dispatch.Signal(providing_args=["aContract", "aUser"])



contract_new_init = django.dispatch.Signal(providing_args=["terms_form"])
contract_needs_participants = django.dispatch.Signal(providing_args=["aContract"])
