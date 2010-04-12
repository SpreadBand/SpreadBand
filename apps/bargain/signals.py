import django.dispatch

contract_concluded = django.dispatch.Signal(providing_args=["aContract"])
