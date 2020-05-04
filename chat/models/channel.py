import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.urls import reverse
from .managers import ChannelManager


class Channel(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    owner = models.ForeignKey(
        get_user_model(), verbose_name=_('owner'), related_name='channels', on_delete=models.DO_NOTHING
    )
    access_code = models.UUIDField(verbose_name=_('access code'), default=uuid.uuid4, editable=False)
    is_private = models.BooleanField(verbose_name=_('is private'), default=True)

    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(_('slug'), max_length=250, unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(verbose_name=_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=_('updated at'), auto_now=True, editable=False)

    objects = ChannelManager()

    class Meta:
        db_table = 'leh_channels'
        indexes = [models.Index(fields=['name', 'owner', 'slug', 'created_at'])]
        ordering = ['-created_at', 'name']

    @property
    def is_public(self):
        return not self.is_private

    @property
    def participants(self):
        return self.members.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.name}-{str(self.uuid)[-12:]}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.slug}'

    def get_absolute_url(self):
        return reverse('channel-detail', kwargs={'slug': self.slug})
