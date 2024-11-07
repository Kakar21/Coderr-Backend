from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsReviewerOrReadOnly(BasePermission):
    """
    Allows only the `reviewer` of a review to edit or delete it.
    Other users have read-only access.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.reviewer == request.user or request.user.is_superuser


class IsCustomerOrReadOnly(BasePermission):
    """
    Allows only customers to create reviews.
    Other users have read-only access.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.profile.type == 'customer'

