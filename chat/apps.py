from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChatConfig(AppConfig):
    name = 'leh_chat'
    verbose_name = _("Chat")

    def ready(self):
        from .models import signals
