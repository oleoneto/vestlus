from django.dispatch import receiver
from django.db.models.signals import post_save
from ...models import Membership, Channel


@receiver(post_save, sender=Channel, dispatch_uid="create_channel_member")
def create_member(sender, **kwargs):
    instance = kwargs.get('instance')

    # When a channel is created, ensure the owner of the channel is made a member of it.
    if kwargs.get('created', True):
        Membership.objects.get_or_create(
            user_id=instance.owner_id,
            channel_id=instance.id,
            invited_by_id=instance.owner_id,
            is_admin=True
        )
