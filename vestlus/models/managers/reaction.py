from django.db import models
from django.db.models import Q


class ReactionManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().prefetch_related()

    def get_for_user(self, user):
        return self.get_queryset().filter(
            Q(user=user) |
            Q(message__sender=user)
        ).distinct()
