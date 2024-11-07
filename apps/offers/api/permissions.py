from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow the owner of an offer to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user or request.user.is_superuser

class IsBusinessOrReadOnly(BasePermission):
    """
    Allows only business users to create offers.
    Other users have read-only access.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.profile.type == 'business'
