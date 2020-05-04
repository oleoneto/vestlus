from rest_framework import serializers
from .mixins import ExcludeTimestampMixin, ExcludeTimestampAndPolymorphicMixin
from ..models import PrivateMessage, GroupMessage, Reaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta(ExcludeTimestampMixin.Meta):
        model = Reaction
        read_only_fields = ('message', 'user')


# Private and Group Messages

class MessageSerializer(serializers.ModelSerializer):

    reactions = ReactionSerializer(many=True, required=False, allow_null=True)

    class Meta(ExcludeTimestampAndPolymorphicMixin.Meta):

        read_only_fields = (
            'sender',
        )


class PrivateMessageSerializer(MessageSerializer):
    class Meta(MessageSerializer.Meta):
        model = PrivateMessage


class GroupMessageSerializer(MessageSerializer):

    class Meta(MessageSerializer.Meta):
        model = GroupMessage

        read_only_fields = (
            'sender',
            'channel',
        )
