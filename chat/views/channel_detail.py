from django.utils import timezone
from django.views.generic import DetailView
from django.urls import path
from .routes import routes
from ..models import Channel


class ChannelDetailView(DetailView):
    model = Channel
    template_name = 'channel_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


routes.append(
    path('channels/<slug:slug>', ChannelDetailView.as_view(), name='channel-detail')
)
