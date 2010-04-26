import django.dispatch

contract_concluded = django.dispatch.Signal(providing_args=["aContract"])

contract_new_init = django.dispatch.Signal(providing_args=["terms_form"])
