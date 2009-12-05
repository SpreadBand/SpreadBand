import authority
from authority import permissions

from .models import Band

class BandPermission(permissions.BasePermission):
    label = 'band_permission'
    checks = ('change',)

authority.register(Band, BandPermission)


