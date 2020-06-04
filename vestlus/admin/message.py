from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin
from polymorphic.admin import PolymorphicChildModelAdmin
from polymorphic.admin import PolymorphicChildModelFilter
from ..models.message import Message
from ..models.message import PrivateMessage
from ..models.message import GroupMessage
from .inlines.message import MessageInline
from .inlines.message import ReactionInline
from .actions import make_read, make_unread


@admin.register(PrivateMessage)
class PrivateMessageAdmin(PolymorphicChildModelAdmin):
    base_model = PrivateMessage
    show_in_index = True
    inlines = [MessageInline, ReactionInline]
    actions = [make_read, make_unread]
    list_display = [
        'slug',
        'sender',
        'receiver',
        'created_at',
        'updated_at',
    ]


@admin.register(GroupMessage)
class GroupMessageAdmin(PolymorphicChildModelAdmin):
    base_model = GroupMessage
    show_in_index = True
    inlines = [MessageInline, ReactionInline]
    list_display = [
        'slug',
        'sender',
        'channel',
        'parent',
        'created_at',
        'updated_at',
    ]


@admin.register(Message)
class MessageAdmin(PolymorphicParentModelAdmin):
    base_model = Message
    inlines = [MessageInline, ReactionInline]
    list_filter = (PolymorphicChildModelFilter,)
    child_models = (PrivateMessage, GroupMessage)
    list_display = [
        'slug',
        'id',
        'sender',
        'parent',
        'created_at',
        'updated_at',
    ]

    # Ensure current user is assigned as sender.
    def save_model(self, request, obj, form, change):
        if not obj.sender_id:
            obj.sender = request.user
        obj.save()
