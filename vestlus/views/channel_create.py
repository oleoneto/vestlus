from django.utils import timezone
from django.views.generic import CreateView
from django.urls import path
from .routes import routes
from ..models import Channel
from ..forms import ChannelForm


class ChannelCreateView(CreateView):
    model = Channel
    fields = ('name', 'is_private',)
    template_name = 'channel_create.html'
    context_object_name = 'channel'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


routes.append(
    path('channels/new/', ChannelCreateView.as_view(), name='channel-create')
)
