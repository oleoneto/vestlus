from django.utils import timezone
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.urls import path
from .routes import routes
from ..models import Message, GroupMessage


@method_decorator([login_required], name='dispatch')
class MessageDeleteView(DeleteView):
    model = Message
    context_object_name = 'message'
    template_name = 'message_delete.html'

    def get_success_url(self):
        return reverse('vestlus:message-list')


routes.append(
    path('messages/<slug:slug>/delete', MessageDeleteView.as_view(), name='message-delete')
)


@method_decorator([login_required], name='dispatch')
class ChannelMessageDeleteView(DeleteView):
    model = GroupMessage
    context_object_name = 'group_message'
    template_name = 'message_delete.html'

    def get_success_url(self):
        return reverse('vestlus:channel-detail', kwargs={'slug': self.kwargs['channel']})


routes.append(
    path(
        'channels/<slug:channel>/messages/<slug:slug>/delete',
        ChannelMessageDeleteView.as_view(),
        name='channel-message-delete'
    )
)
