from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from haystack.signals import RealtimeSignalProcessor
from haystack.management.commands import update_index
from ...models import Channel, Message, GroupMessage, PrivateMessage


# @receiver([post_save, post_delete], sender=Channel, dispatch_uid='update_channel_index')
def update_search_indexes(sender, **kwargs):
    """Call haystack.update_index to update backend search indexes"""
    instance = kwargs.get('instance')

    if kwargs.get('created', True):
        print('Created new instance...')
    elif kwargs.get('updated', True):
        print('Update instance...')
