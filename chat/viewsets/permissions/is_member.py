from rest_framework import permissions
from ...models import Channel


class IsMemberOrNoAccess(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        channel_pk = view.kwargs['channels_pk']

        try:
            channel = Channel.objects.get(pk=channel_pk)
            return (not channel.is_private) or \
                request.user in channel.members.all()
        except Channel.DoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        return request.user in obj.members
