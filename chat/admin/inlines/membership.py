from django.contrib import admin
from ...models import Membership


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
