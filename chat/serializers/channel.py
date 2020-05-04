from rest_framework import serializers
from ..models import Channel


class ChannelSerializer(serializers.ModelSerializer):

    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    total_messages = serializers.IntegerField(
        source='get_total_messages',
        read_only=True
    )

    class Meta:
        model = Channel
        fields = "__all__"

        read_only_fields = (
            'owner',
        )

        def get_total_messages(self, obj):
            return obj.messages.count()
