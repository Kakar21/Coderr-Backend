from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsCustomerOrReadOnly(BasePermission):
    """
    Allows only customers to create orders.
    Other users have read-only access.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.profile.type == 'customer'