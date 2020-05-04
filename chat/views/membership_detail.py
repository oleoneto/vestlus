from django.utils import timezone
from django.views.generic import DetailView
from django.urls import path
from .routes import routes
from ..models import Membership


class MembershipDetailView(DetailView):
    model = Membership
    template_name = 'membership_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


routes.append(
    path('memberships/<slug:slug>', MembershipDetailView.as_view(), name='membership-detail')
)
