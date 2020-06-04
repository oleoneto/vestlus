from django.db import models
from django.db.models import Q


class MembershipManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().prefetch_related()

    def none(self):
        return self.get_queryset().filter(user_id=0)

    def me(self, user):
        return self.get_queryset().filter(user=user)

    def get_for_channel(self, channel):
        return self.get_queryset().filter(
            Q(channel=channel) &
            Q(channel__is_private=False)
        ).distinct()

    def get_for_user(self, user):
        return self.get_queryset().filter(
            Q(user=user) |
            Q(channel__members__user=user)
        ).distinct()

    # Get membership information if:
    # - User is member of channel or
    # - Channel is open to the public
    def get_for_channel_and_user(self, channel, user):
        return self.get_queryset().filter(
            (
                Q(channel=channel) &
                Q(channel__members__user=user)
            ) |
            (
                Q(channel=channel) &
                Q(channel__is_private=False)
            )
        ).distinct()
