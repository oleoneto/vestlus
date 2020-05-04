from django.forms import forms
from ..models import Message, PrivateMessage, GroupMessage


class MessageForm(forms.Form):
    class Meta:
        model = Message
        fields = '__all__'


class PrivateMessageForm(forms.Form):
    class Meta:
        model = PrivateMessage
        fields = '__all__'


class GroupMessageForm(forms.Form):
    class Meta:
        model = GroupMessage
        fields = '__all__'
