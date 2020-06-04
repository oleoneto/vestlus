import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.urls import reverse
from .managers import MembershipManager
from .channel import Channel


class Membership(models.Model):
    channel = models.ForeignKey(
        Channel, verbose_name=_('channel'), related_name='members', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        get_user_model(), verbose_name=_('user'), related_name='memberships', on_delete=models.CASCADE
    )
    invited_by = models.ForeignKey(
        get_user_model(),
        verbose_name=_('invited by'), related_name='invitees', on_delete=models.DO_NOTHING,
        blank=True, null=True, help_text='The user who invited this one'
    )
    is_admin = models.BooleanField(
        default=False, verbose_name=_('is admin'), help_text='Defines if user has admin privileges'
    )

    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(_('slug'), max_length=250, unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('uploaded at'), auto_now=True, editable=False)

    objects = MembershipManager()

    class Meta:
        db_table = 'vestlus_channel_members'
        indexes = [models.Index(fields=['channel', 'user', 'invited_by', 'slug', 'created_at'])]
        ordering = ['-created_at', 'user']
        unique_together = ('channel', 'user')

    @property
    def channel_owner(self):
        return self.channel.owner

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.user}-{str(self.uuid)[-12:]}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.slug}'
    
    def get_absolute_url(self):
        return reverse('vestlus:membership-detail', kwargs={'slug': self.slug})
