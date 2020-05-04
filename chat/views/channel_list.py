from django.utils import timezone
from django.views.generic import ListView
from django.urls import path
from .routes import routes
from ..models import Channel


class ChannelListView(ListView):
    model = Channel
    template_name = 'channel_list.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


routes.append(
    path('channels/', ChannelListView.as_view(), name='channel-list')
)
