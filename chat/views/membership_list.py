from django.utils import timezone
from django.views.generic import ListView
from django.urls import path
from .routes import routes
from ..models import Membership


class MembershipListView(ListView):
    model = Membership
    template_name = 'membership_list.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


routes.append(
    path('memberships/', MembershipListView.as_view(), name='membership-list')
)
