from django.db.models import Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.urls import path
from .routes import routes
from ..models import Channel, Message


@method_decorator([login_required], name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        channels = Channel.objects.get_for_user(user=self.request.user)
        messages = Message.custom_objects.get_for_user(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context['channels'] = channels
        context['messages'] = messages
        return context


routes.append(
    path('', IndexView.as_view(), name='chat-index')
)
