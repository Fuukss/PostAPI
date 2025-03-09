from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerIP(BasePermission):
    """
    Umożliwia modyfikację rekordu wyłącznie przez autora (sprawdzany przez adres IP).
    Dostęp do metod bezpiecznych (GET, HEAD, OPTIONS) jest otwarty.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.META.get('REMOTE_ADDR') == obj.author_ip
