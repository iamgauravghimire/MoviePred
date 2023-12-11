from rest_framework.permissions import BasePermission
from rest_framework import permissions
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the requesting user is the owner of the movie
        return obj.movie_owner == request.user