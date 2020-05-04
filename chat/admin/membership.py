from django.contrib import admin
from ..models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'channel',
        'user',
        'is_admin',
        'created_at',
        'updated_at',
    ]
