from django.contrib import admin
from ...models import Channel


class ChannelInline(admin.StackedInline):
    model = Channel
    extra = 0
