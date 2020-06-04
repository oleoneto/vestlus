# vestlus:admin:actions


def make_read(model, request, queryset):
    queryset.update(read=True)


make_read.short_description = "Mark as read"


def make_unread(model, request, queryset):
    queryset.update(read=False)


make_unread.short_description = "Mark as unread"


def make_private(model, request, queryset):
    queryset.update(is_private=True)


make_private.short_description = "Make private"


def make_public(model, request, queryset):
    queryset.update(is_private=False)


make_public.short_description = "Make public"
