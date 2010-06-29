import django.dispatch

# When a contract is created
contract_new = django.dispatch.Signal(providing_args=["aContract"])

# When someone updates a contract
contract_amended = django.dispatch.Signal(providing_args=["aContract", "aParticipant"])

# When someone (dis)approve a contract
contract_approved = django.dispatch.Signal(providing_args=["aContract", "aParticipant"])
contract_disapproved = django.dispatch.Signal(providing_args=["aContract", "aParticipant"])

# When a contract is concluded
contract_concluded = django.dispatch.Signal(providing_args=["aContract", "aUser"])

