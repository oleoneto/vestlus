from django.utils import timezone
from django.views.generic import ListView
from django.urls import path
from .routes import routes
from ..models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'message_list.html'
    paginate_by = 20

    def get_queryset(self):
        return Message.objects.get_for_user(
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


routes.append(
    path('messages/', MessageListView.as_view(), name='message-list')
)
