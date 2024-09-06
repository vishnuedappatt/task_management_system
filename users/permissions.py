from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated

class IsAdminUser(BasePermission):
    def has_permission(self, request,view):
        return request.user and request.user.is_admin


class IsStandardUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and not request.user.is_admin