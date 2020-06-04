from django.utils import timezone
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.urls import path
from .routes import routes
from ..models import Channel


@method_decorator([login_required], name='dispatch')
class ChannelDeleteView(DeleteView):
    model = Channel
    context_object_name = 'channel'
    template_name = 'channel_delete.html'

    def get_queryset(self):
        return Channel.objects.get_for_user(user=self.request.user)

    def get_success_url(self):
        return reverse('vestlus:channel-list')


routes.append(
    path('channels/<slug:slug>/delete', ChannelDeleteView.as_view(), name='channel-delete')
)
