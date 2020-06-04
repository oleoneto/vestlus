from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from .permissions.is_sender import IsSenderOrReadOnly
from .permissions.is_member import IsMemberOrNoAccess
from .router import router
from ..models import Channel
from ..models import Message
from ..models import PrivateMessage
from ..models import GroupMessage
from ..models import Reaction
from ..serializers import PrivateMessageSerializer
from ..serializers import GroupMessageSerializer
from ..serializers import ReactionSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = PrivateMessage.objects.all()
    serializer_class = PrivateMessageSerializer
    permission_classes = [IsSenderOrReadOnly]
    search_fields = ['^content']
    permit_list_expands = ['sender', 'receiver', 'parent']
    filter_fields = ['id', 'sender', 'receiver', 'created_at']
    # lookup_field = 'uuid'

    def get_queryset(self):
        user = self.request.user

        return self.filter_queryset(
            Message.objects.get_for_user(
                user=user
            )
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    @action(detail=False, methods=['get'])
    def notes(self, request):
        user = request.user
        messages = Message.objects.private_notes(user=user)
        messages = self.filter_queryset(messages)

        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)


class GroupMessageViewSet(viewsets.ModelViewSet):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsSenderOrReadOnly |
        IsMemberOrNoAccess
    ]
    search_fields = ['^content']
    permit_list_expands = ['sender', 'parent']
    filter_fields = ['id', 'sender', 'parent', 'created_at']
    # lookup_field = 'uuid'

    def initial(self, request, *args, **kwargs):
        user = request.user
        get_object_or_404(Channel.objects.get_for_user(user=user), pk=kwargs['channels_pk'])
        return super().initial(request, args, kwargs)

    def get_queryset(self):
        user = self.request.user

        return GroupMessage.objects.get_for_channel(
            channel=self.kwargs['channels_pk'],
            user=user
        )

    def perform_create(self, serializer):
        user = self.request.user

        channel = Channel.objects.get(
            id=self.kwargs['channels_pk']
        )

        serializer.save(
            channel_id=channel.id,
            sender=user
        )


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.queryset.filter(
            message=self.kwargs['messages_pk'],
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(
            message_id=self.kwargs['messages_pk'],
            user=self.request.user,
        )


router.register('messages', MessageViewSet)

router.register('group-messages', GroupMessageViewSet)
