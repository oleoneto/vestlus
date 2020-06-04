from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class VestlusConfig(AppConfig):
    name = 'vestlus'
    verbose_name = _("Chat")

    def ready(self):
        from .models import signals
