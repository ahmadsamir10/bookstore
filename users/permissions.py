from rest_framework.permissions import BasePermission


class IsClient(BasePermission):
    """
    Custom permission to only allow Active-Client-Type users
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_active and user.user_type == "client"
