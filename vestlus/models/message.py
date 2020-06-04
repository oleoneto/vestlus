import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify, truncatewords
from django.urls import reverse
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from .channel import Channel
from .managers import MessageManager
from .managers import GroupMessageManager
from .managers import ReactionManager


class Message(PolymorphicModel):
    sender = models.ForeignKey(
        get_user_model(),
        verbose_name=_('sender'),
        related_name='sent_messages',
        on_delete=models.PROTECT,
        help_text='The user who authored the message'
    )
    parent = models.ForeignKey(
        'self',
        verbose_name=_('parent'),
        related_name='replies',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text='The main message in a message thread'
    )
    content = models.TextField(_('content'))

    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(_('slug'), max_length=250, unique=True, editable=False, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('uploaded at'), auto_now=True, editable=False)

    objects = PolymorphicManager()
    custom_objects = MessageManager()

    class Meta:
        db_table = 'vestlus_messages'
        indexes = [models.Index(fields=['created_at', 'sender', 'parent'])]
        ordering = ['-created_at', 'sender']

    @property
    def preview(self):
        return f'{truncatewords(self.content, 20)}...'

    @property
    def avatar(self):
        try:
            return self.sender.photo.url
        except AttributeError:
            return 'https://github.com/octocat.png'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{str(self.uuid)[-12:]}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.slug}'

    def get_absolute_url(self):
        return reverse('vestlus:message-detail', kwargs={'slug': self.slug})


class PrivateMessage(Message):
    receiver = models.ForeignKey(
        get_user_model(),
        verbose_name=_('receiver'),
        related_name='received_messages',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text='The user this message will be sent to'
    )
    read = models.BooleanField(
        default=False,
        verbose_name=_('read'),
        help_text='Indicates whether or not the recipient has visualized the message'
    )

    class Meta:
        db_table = 'vestlus_private_messages'
        indexes = [models.Index(fields=['receiver', 'read'])]


class GroupMessage(Message):
    channel = models.ForeignKey(
        Channel,
        verbose_name=_('channel'),
        related_name='conversations',
        on_delete=models.CASCADE,
        help_text='The channel associated with this message'
    )

    custom_objects = GroupMessageManager()

    class Meta:
        db_table = 'vestlus_group_messages'
        indexes = [models.Index(fields=['channel'])]
        ordering = ['-created_at', 'channel']


class Reaction(models.Model):
    message = models.ForeignKey(
        Message,
        verbose_name=_('message'),
        related_name='reactions',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        get_user_model(),
        verbose_name=_('user'),
        related_name='reactions',
        on_delete=models.CASCADE,
        help_text='The user who reacted to the message'
    )
    reaction = models.CharField(
        max_length=32,
        verbose_name=_('reaction'),
        help_text='Emoji reaction code as unicode'
    )

    # Default fields. Used for record-keeping.
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('uploaded at'), auto_now=True, editable=False)

    objects = ReactionManager()

    class Meta:
        db_table = 'vestlus_message_reactions'
        ordering = ['-created_at', 'message', 'user']
