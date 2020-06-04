# vestlus:serializers:mixins
from rest_framework import serializers


class ChatRelatedField(serializers.RelatedField):
    """
    Query only chats for the logged-in user.
    """
    def get_queryset(self):
        request = self.context['request']
        user_id = request.user.id
        return super().get_queryset().filter(owner=user_id)


class ChatSerializerMixin(object):
    serializer_related_field = ChatRelatedField
