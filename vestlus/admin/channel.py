from django.contrib import admin
from ..models import Channel
from .inlines import GroupMessageInline, MembershipInline
from .actions import make_private, make_public


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    actions = [make_private, make_public]
    inlines = [GroupMessageInline, MembershipInline]
    list_display = [
        'slug',
        'id',
        'name',
        'total_members',
        'is_private',
        'owner',
        'created_at',
        'updated_at',
        'uuid',
    ]

    def get_queryset(self, request):
        return Channel.objects.get_for_user(
            user=request.user
        )

    def has_view_or_change_permission(self, request, obj=None):
        if obj is not None:
            return obj.owner == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return obj.owner == request.user
        return True

    # Ensure current user is assigned as owner of channel.
    def save_model(self, request, obj, form, change):
        if not obj.owner_id:
            obj.owner = request.user
        obj.save()
