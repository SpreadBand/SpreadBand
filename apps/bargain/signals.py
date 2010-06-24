import django.dispatch

contract_concluded = django.dispatch.Signal(providing_args=["aContract", "aUser"])


# When a contract is created
contract_new = django.dispatch.Signal(providing_args=["aContract"])

# Unused for now, should be removed
contract_needs_participants = django.dispatch.Signal(providing_args=["aContract"])
