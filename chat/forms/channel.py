from django.forms import forms
from ..models import Channel


class ChannelForm(forms.Form):
    class Meta:
        model = Channel
        fields = '__all__'
