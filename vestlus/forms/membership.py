from django.forms import forms
from ..models import Membership


class MembershipForm(forms.Form):
    class Meta:
        model = Membership
        fields = '__all__'
