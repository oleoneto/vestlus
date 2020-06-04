from django.utils import timezone
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView
from django.urls import path
from .routes import routes
from ..models import Channel
from ..forms import GroupMessageForm


@method_decorator([login_required], name='dispatch')
class ChannelDetailView(DetailView, CreateView):
    model = Channel
    context_object_name = 'channel'
    template_name = 'channel_detail.html'
    form_class = GroupMessageForm

    def form_valid(self, form):
        form.instance.channel = self.get_object()
        form.instance.sender = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(viewname='vestlus:channel-detail', kwargs={'slug': self.get_object().slug})

    def get_queryset(self):
        return Channel.objects.get_for_user(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object is not None:
            context['user_in_admins'] = self.get_object().admins.filter(user=self.request.user)
        return context


routes.append(
    path('channels/<slug:slug>', ChannelDetailView.as_view(), name='channel-detail')
)
