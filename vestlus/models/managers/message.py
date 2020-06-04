from django.db.models import Q
from polymorphic.managers import PolymorphicManager


class MessageManager(PolymorphicManager):
    def get_queryset(self):
        qs = super(MessageManager, self).get_queryset().prefetch_related()
        return qs

    # `Private notes` are messages with no recipient or where the sender is the recipient
    def private_notes(self, user):
        return self.get_queryset().filter(
            Q(sender=user) &
            Q(
                Q(PrivateMessage___receiver=user) |
                Q(PrivateMessage___receiver__isnull=True)
            ) &
            Q(GroupMessage___channel__isnull=True)
        )

    def get_private_messages_for_user(self, user):
        return self.get_queryset().filter(
            Q(PrivateMessage___sender=user) |
            Q(PrivateMessage___receiver=user)
        )

    # Get messages that match the following criteria:
    # - Message was sent by user
    # - Message was received by user
    # - Message was sent to a group of which the user is a member
    def get_for_user(self, user):
        return self.get_queryset().filter(
            Q(sender=user) |
            Q(
                Q(PrivateMessage___receiver=user) |
                Q(GroupMessage___channel__members__user=user)
            )
        ).distinct()


class GroupMessageManager(PolymorphicManager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related()

    def most_recent(self):
        return self.get_queryset()[:20]

    # Get messages that match the following criteria:
    # - Message was sent by user
    # - Message was received by user
    # - Message was sent to a group of which the user is a member
    def get_for_user(self, user):
        return self.get_queryset().filter(
            Q(sender=user) |
            Q(channel__members__user=user)
        ).distinct()

    # Get messages that match the following criteria:
    # - Message was sent to the channel and
    # - Channel is either public or
    # - Message was sent to a group of which the user is a member
    def get_for_channel(self, channel, user):
        return self.get_queryset().filter(
            Q(channel=channel) &
            (
                Q(channel__is_private=False) |
                Q(channel__members__user=user)
            )
        ).distinct()

    def public(self):
        return self.get_queryset().filter(
            Q(GroupMessage___channel__is_private=False)
        )

    def private(self):
        return self.get_queryset().filter(is_private=True)
