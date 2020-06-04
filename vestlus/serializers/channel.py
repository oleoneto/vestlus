from rest_framework import serializers
from ..models import Channel
from .message import GroupMessageSerializer


class ChannelSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    conversations = GroupMessageSerializer(many=True, allow_null=True)

    class Meta:
        model = Channel
        fields = (
            'id',
            'uuid',
            'slug',
            'owner',
            'name',
            'is_private',
            'created_at',
            'updated_at',
            'total_messages',
            'conversations',
        )
        # exclude = ('access_code',)

        read_only_fields = (
            'owner',
        )
