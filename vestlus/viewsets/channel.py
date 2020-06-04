from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .router import router
from ..models import Channel
from ..serializers import ChannelSerializer
from .message import GroupMessage, GroupMessageViewSet, GroupMessageSerializer
from .membership import MembershipViewSet
from .permissions.is_admin import IsChannelOwnerOrAdminOrReadOnly
from .mixin.detail_action import DetailActionMixin
from .mixin.non_detail_action import NonDetailActionMixin


class ChannelViewSet(viewsets.ModelViewSet, DetailActionMixin, NonDetailActionMixin):
    queryset = Channel.objects.public()
    serializer_class = ChannelSerializer
    permission_classes = [IsChannelOwnerOrAdminOrReadOnly]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        return Channel.objects.get_for_user(
            user=self.request.user
        )

    def perform_create(self, serializer):
        owner = self.request.user
        channel = serializer.save(owner=owner)

        # When a channel is created, a membership is also created via a signal.

    @action(detail=False, methods=['get'])
    def me(self, request):
        return self.non_detail_action(self.get_queryset())

    @action(detail=True)
    def messages(self, request, uuid):
        # note the change from pk to uuid in signature
        objects = GroupMessage.objects.filter(channel=self.get_object())
        return self.detail_action(objects, GroupMessageSerializer)


router.register('channels', ChannelViewSet)
