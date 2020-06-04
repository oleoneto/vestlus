from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):

        # Non-owners can READ content, but will not be able to UPDATE or DELETE
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
