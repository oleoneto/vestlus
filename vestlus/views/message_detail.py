from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import path
from .routes import routes
from ..models import Message


@method_decorator([login_required], name='dispatch')
class MessageDetailView(UserPassesTestMixin, DetailView):
    model = Message
    template_name = 'message_detail.html'
    context_object_name = 'message'

    def test_func(self):
        user = self.request.user
        message = self.get_object()
        return (
            user == message.sender or
            user == message.receiver
        )
        # return user == message.sender or user == message.receiver

    # def get_queryset(self):
    #     queryset = super(MessageDetailView, self).get_queryset()
    #     return queryset.get_for_user(user=self.request.user)


routes.append(
    path('messages/<slug:slug>', MessageDetailView.as_view(), name='message-detail')
)
