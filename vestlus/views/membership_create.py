from django.utils import timezone
from django.shortcuts import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import path
from .routes import routes
from ..models import Membership, Channel


@method_decorator([login_required], name='dispatch')
class MembershipCreateView(CreateView):
    model = Membership
    context_object_name = 'membership'
    template_name = 'membership_create.html'
    fields = ('user', 'is_admin',)

    def form_valid(self, form):
        channel = Channel.objects.get(slug=self.kwargs['slug'])
        form.instance.channel = channel
        form.instance.invited_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        channel = Channel.objects.get(slug=self.kwargs['slug'])
        context = super().get_context_data(**kwargs)
        context['channel'] = channel
        return context

    def get_success_url(self):
        return reverse(viewname='vestlus:channel-detail', kwargs=self.kwargs)


routes.append(
    path('memberships/<slug:slug>/new/', MembershipCreateView.as_view(), name='membership-create')
)
