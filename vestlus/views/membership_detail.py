from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.urls import path
from .routes import routes
from ..models import Membership, GroupMessage


@method_decorator([login_required], name='dispatch')
class MembershipDetailView(DetailView):
    model = Membership
    context_object_name = 'membership'
    template_name = 'membership_detail.html'

    # def get_queryset(self):
    #     return Membership.objects.get_for_user(user=self.request.user)

    def get_context_data(self, **kwargs):
        messages = GroupMessage.custom_objects.get_for_channel(
            channel=self.object.channel,
            user=self.object.user
        )

        context = super().get_context_data(**kwargs)
        context['messages'] = messages
        return context


routes.append(
    path('memberships/<slug:slug>', MembershipDetailView.as_view(), name='membership-detail')
)
