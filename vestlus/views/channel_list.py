from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.urls import path
from .routes import routes
from ..models import Channel


@method_decorator([login_required], name='dispatch')
class ChannelListView(ListView):
    model = Channel
    template_name = 'channel_list.html'
    context_object_name = 'channels'
    paginate_by = 20

    def get_queryset(self):
        return Channel.objects.get_for_user(
            user=self.request.user,
        ).filter(members__user=self.request.user)

    def get_context_data(self, **kwargs):
        recommended_channels = Channel.objects.get_suggestions_for_user(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['recommended_channels'] = recommended_channels
        return context


routes.append(
    path('channels/', ChannelListView.as_view(), name='channel-list')
)
