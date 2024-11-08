from rest_framework.permissions import BasePermission


class IsCustomerForPost(BasePermission):
    """
    Allows only customers to create orders.
    Other users have read-only access.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.profile.type == 'customer'
        return True


class IsStaffOrReadOnlyForDestroy(BasePermission):
    """
    Allows deletion (`destroy`) only for staff members.
    Other methods (GET, PATCH, etc.) are accessible to all.
    """     
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_staff
        return True
