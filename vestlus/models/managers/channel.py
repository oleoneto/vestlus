from django.db import models
from django.db.models import Q


class ChannelManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().prefetch_related()

    def public(self):
        return self.get_queryset().filter(
            is_private=False
        )

    def private(self):
        return self.get_queryset().filter(
            is_private=True
        )

    def owned(self, user):
        return self.get_queryset().filter(
            owner=user
        )

    # User can see channels that match any of the following:
    # - channel is owned by user
    # - user is member of channel
    # - channel is open to the public
    def get_for_user(self, user):
        return self.get_queryset().filter(
            Q(owner=user) |
            Q(members__user=user) |
            Q(is_private=False)
        ).distinct()

    # User can see channels that match any of the following:
    # - channel is public
    # - user is not in channel
    def get_suggestions_for_user(self, user):
        return self.get_queryset().filter(
            Q(is_private=False) &
            (
                ~Q(owner=user) |
                ~Q(members__user=user)
            )
        ).distinct()
