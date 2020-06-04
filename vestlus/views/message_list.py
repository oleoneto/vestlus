from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.urls import path
from .routes import routes
from ..models import Message


@method_decorator([login_required], name='dispatch')
class MessageListView(ListView):
    model = Message
    template_name = 'message_list.html'
    context_object_name = 'messages'
    paginate_by = 20

    def get_queryset(self):
        return Message.custom_objects.get_for_user(
            user=self.request.user
        )


routes.append(
    path('messages/', MessageListView.as_view(), name='message-list')
)
