from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.urls import path
from .routes import routes
from ..models import Membership


@method_decorator([login_required], name='dispatch')
class MembershipListView(ListView):
    model = Membership
    template_name = 'membership_list.html'
    context_object_name = 'memberships'
    paginate_by = 20

    def get_queryset(self):
        return Membership.objects.get_for_user(
            user=self.request.user
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


routes.append(
    path('memberships/', MembershipListView.as_view(), name='membership-list')
)
