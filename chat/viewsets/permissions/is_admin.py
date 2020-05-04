from rest_framework import permissions


class IsChannelOwnerOrAdminOrReadOnly(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):

        # Non-owners and non-admins can READ content, but will not be able to UPDATE or DELETE
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.owner == request.user:
            return True
        membership = obj.members.get(user=request.user)
        return membership.is_admin
