from rest_framework.permissions import BasePermission



class IsXanAuthenticated(BasePermission):
    """
    Allows access only to xan_authenticated users.
    """

    def has_permission(self, request, view): # type: ignore
        return request.service_name is not None


