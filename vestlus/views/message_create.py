from django.utils import timezone
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import CreateView, View, DetailView
from django.urls import path
from .mixins import AjaxableResponseMixin
from .routes import routes
from ..models import Message, GroupMessage, Channel
from ..forms import GroupMessageForm


@method_decorator([login_required], name='dispatch')
class ChannelMessageCreateView(AjaxableResponseMixin, CreateView):
    form_class = GroupMessageForm
    template_name = 'message_create.html'
    context_object_name = 'message'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        slug = kwargs.get('slug', None)

        if slug is not None:
            self.channel = Channel.objects.get(slug=slug)

    def get_success_url(self):
        return reverse(viewname='vestlus:channel-detail', kwargs={'slug': self.channel.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs['slug']
        self.channel = Channel.objects.get(slug=slug)

        context['channel'] = self.channel
        return context


routes.append(
    path('channels/<slug:slug>/messages/new/', ChannelMessageCreateView.as_view(), name='message-create')
)
