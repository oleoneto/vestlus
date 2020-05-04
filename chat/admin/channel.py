from django.contrib import admin
from ..models import Channel
from .actions import make_private, make_public


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    actions = [make_private, make_public]
    list_display = [
        'id',
        'name',
        'is_private',
        'owner',
        'created_at',
        'updated_at',
        'uuid'
    ]

    # Ensure current user is assigned as owner of channel.
    def save_model(self, request, obj, form, change):
        if not obj.owner_id:
            obj.owner = request.user
        obj.save()
