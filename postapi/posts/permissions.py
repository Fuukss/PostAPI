from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerIP(BasePermission):
    """
    Allows modification of a record only by its owner, verified by the IP address.
    Access to safe methods (GET, HEAD, OPTIONS) is granted to all users.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.META.get('REMOTE_ADDR') == obj.author_ip
