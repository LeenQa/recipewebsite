from rest_framework import permissions
from .models import Recipe


class IsLoggedUser(permissions.BasePermission):
    message = "Only update/delete records you created"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user