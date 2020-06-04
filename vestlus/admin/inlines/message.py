from django.contrib import admin
from ...models import (
    Message,
    PrivateMessage,
    GroupMessage,
    Reaction
)


class MessageInline(admin.StackedInline):
    model = Message
    extra = 0


class PrivateMessageInline(admin.StackedInline):
    model = PrivateMessage
    extra = 0


class GroupMessageInline(admin.StackedInline):
    model = GroupMessage
    extra = 0


class ReactionInline(admin.StackedInline):
    model = Reaction
    extra = 0
