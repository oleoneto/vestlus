from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_nested import routers
from .router import router
from ..models import Channel
from ..serializers import ChannelSerializer
from .message import GroupMessageViewSet
from .membership import MembershipViewSet
from .permissions.is_admin import IsChannelOwnerOrAdminOrReadOnly


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.public()
    serializer_class = ChannelSerializer
    permission_classes = [IsChannelOwnerOrAdminOrReadOnly]

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
        channels = self.get_queryset()

        page = self.paginate_queryset(channels)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(channels, many=True)
        return Response(serializer.data)


router.register('channels', ChannelViewSet)

channels_router = routers.NestedSimpleRouter(
    router,
    r'channels',
    lookup='channels'
)

channels_router.register(
    r'members',
    MembershipViewSet,
    basename='members'
)

channels_router.register(r'messages', GroupMessageViewSet)
