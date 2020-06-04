from django.contrib import admin
from ..models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = [
        'slug',
        'id',
        'channel',
        'channel_owner',
        'user',
        'is_admin',
        'created_at',
        'updated_at',
    ]

    def get_queryset(self, request):
        return Membership.objects.get_for_user(
            user=request.user
        )
